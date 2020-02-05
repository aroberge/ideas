import types

from ideas import import_hook, utils, token_utils
from ideas.console import CONSOLE_NAME

shorten_path = utils.shorten_path
CONSTANTS = {}
DECLARED_FINAL = {}


def make_class(on_prevent_change=True):
    class ModuleWithConstants(types.ModuleType):
        """Special module type that prevents variables identified as constants
           to have their value changed.

           This is used to replace a module __class__ from the default as follows:

               module.__class__ = ModuleWithConstants

           This example only prints a message when an attempt is made to change
           the value of a constant. Alternatively, this could be logged or an
           exception could be raised.
        """

        def __setattr__(self, key, value):
            if (
                key in CONSTANTS[self.__file__]
                or key == key.upper()
                or key in DECLARED_FINAL[self.__file__]
            ):
                if on_prevent_change:
                    if callable(on_prevent_change):
                        on_prevent_change(
                            filename=self.__file__, key=key, value=value, kind="set"
                        )
                    return
            super().__setattr__(key, value)

        def __delattr__(self, key):
            if key in CONSTANTS[self.__file__]:
                if on_prevent_change:
                    if callable(on_prevent_change):
                        on_prevent_change(
                            filename=self.__file__, key=key, kind="delete"
                        )
                    return
            super().__delattr__(key)

    return ModuleWithConstants


class FinalDict(dict):
    """dict subclass which ensures that constants are not over-written.

        Constants are identified in two ways:
           1. names in all UPPERCASE_LETTERS, which is a common convention
           2. variables that were declared to be constant by the inclusion
              of a "Final" type hint.

        Note: We only override methods which could result in changing the value
        of a constant.
    """

    def __init__(self, module_filename, on_prevent_change=True):
        """Initialises the instance"""
        self.__file__ = module_filename
        self.on_prevent_change = on_prevent_change
        super().__init__()

    def __setitem__(self, key, value):
        """Sets self[key] to value.

           If key is identified as a constant, it prevents changing
           its value after initial assignment.
        """
        if key in CONSTANTS[self.__file__]:
            if self.on_prevent_change:
                if callable(self.on_prevent_change):
                    self.on_prevent_change(
                        filename=self.__file__, key=key, value=value, kind="set"
                    )
                return
        if key == key.upper() or key in DECLARED_FINAL[self.__file__]:
            CONSTANTS[self.__file__][key] = value
        return super().__setitem__(key, value)

    def __delitem__(self, key):
        """Deletes self[key] unless key is identified as a constant"""
        if key in CONSTANTS[self.__file__]:
            if self.on_prevent_change:
                if callable(self.on_prevent_change):
                    self.on_prevent_change(
                        filename=self.__file__, key=key, kind="delete"
                    )
                return
            return
        return super().__delitem__(key)

    def setdefault(self, key, default=None):
        """Insert key with a value of default if key is not in the dictionary.

           Prevents changes if the key is identified as a constant.
        """
        if key in CONSTANTS[self.__file__]:
            if self.on_prevent_change:
                if callable(self.on_prevent_change):
                    self.on_prevent_change(
                        filename=self.__file__, key=key, value=default, kind="set"
                    )
                return
        if key == key.upper() or key in DECLARED_FINAL[self.__file__]:
            CONSTANTS[self.__file__][key] = default
        return super().setdefault(key, default)

    def pop(self, key):
        """D.pop(key) -> value, remove specified key and return the corresponding value,
            unless the key is identifed as a constant.

            If key is not found, d is returned if given, otherwise KeyError is raised
        """
        if key in CONSTANTS[self.__file__]:
            if self.on_prevent_change:
                if callable(self.on_prevent_change):
                    self.on_prevent_change(
                        filename=self.__file__, key=key, kind="delete"
                    )
                return CONSTANTS[self.__file__][key]
        return super().pop(key)

    def update(self, mapping_or_iterable=(), **kwargs):
        """Updates the content of the dict from a mapping or an iterable,
            or from a list of keywords arguments.

            Keys identified as constants are prevented from changing.
        """
        if hasattr(mapping_or_iterable, "keys"):
            for key in mapping_or_iterable:
                self.__setitem__(key, mapping_or_iterable[key])
        else:
            for key, value in mapping_or_iterable:
                self.__setitem__(key, value)

        for key in kwargs:
            self.__setitem__(key, kwargs[key])


def transform_source(source, filename=None, **kwargs):
    """Identifies simple assignments with a Final type hint, returning
    the source unchanged.

    The pattern we are looking for is::

        |python_identifier : Final ...

    where ``|`` indicates the beginning of a line.
    """
    if filename not in CONSTANTS:
        CONSTANTS[filename] = {}
    if filename not in DECLARED_FINAL:
        DECLARED_FINAL[filename] = set([])

    for tokens in token_utils.get_lines_of_tokens(source):
        # a line of tokens can start with DEDENT tokens ...
        if token_utils.get_number_nonspace_tokens(tokens) > 3:
            index = token_utils.get_first_nonspace_token_index(tokens)
            first_token = tokens[index]
            if (
                first_token.start_col == 0
                and first_token.is_identifier()
                and tokens[index + 1] == ":"
                and tokens[index + 2] == "Final"
            ):

                DECLARED_FINAL[filename].add(first_token.string)
    return source


def exec_(source, filename=None, globals_=None, callback_params=None, **kwargs):
    locals_ = FinalDict(
        filename, on_prevent_change=callback_params["on_prevent_change"]
    )
    locals_.update(globals_)
    exec(source, locals_)
    globals_.update(locals_)


def on_change_print(filename=None, key=None, value=None, kind=None):
    if kind == "set":
        print(
            "You cannot change the value of %s.%s to %s"
            % (shorten_path(filename), key, value)
        )
    elif kind == "delete":
        print("You cannot delete %s in module %s." % (key, shorten_path(filename)))
    else:
        raise NotImplementedError


def add_hook(on_prevent_change=None):
    """Creates and adds the import hook in sys.meta_path"""
    if on_prevent_change is None:
        on_prevent_change = on_change_print
    callback_params = {"on_prevent_change": on_prevent_change}

    module_class = make_class(**callback_params)
    console_dict = FinalDict(CONSOLE_NAME, on_prevent_change=on_prevent_change)
    CONSTANTS[CONSOLE_NAME] = {}

    hook = import_hook.create_hook(
        module_class=module_class,
        transform_source=transform_source,
        exec_=exec_,
        callback_params=callback_params,
        console_dict=console_dict,
        name=__name__,
    )
    return hook
