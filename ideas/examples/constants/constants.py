import sys
import types

from ideas import import_hook, utils

shorten_path = utils.shorten_path
CONSTANTS = {}
DECLARED_FINAL = {}


class ModuleWithConstants(types.ModuleType):
    """Special module type that prevents variables identified as constants
       to have their value changed.

       This is used to replace a module __class__ from the default as follows:

           module.__class__ = ModuleWithConstants

       This example only prints a message when an attempt is made to change
       the value of a constant. Alternatively, this could be logged or an
       exception could be raised.
    """

    def __setattr__(self, attr, value):
        if attr in CONSTANTS[self.__file__]:
            print(
                "You cannot change the value of %s.%s to %s"
                % (shorten_path(self.__file__), attr, value)
            )
            return
        if attr == attr.upper() or attr in DECLARED_FINAL[self.__file__]:
            print("You cannot add constants to another module.")
            return
        super().__setattr__(attr, value)

    def __delattr__(self, attr):
        if attr in CONSTANTS[self.__file__]:
            print(
                "You cannot delete the constant %s.%s"
                % (shorten_path(self.__file__), attr)
            )
            return

        super().__delattr__(attr)


class FinalDict(dict):
    """dict subclass which ensures that constants are not over-written.

        Constants are identified in two ways:
           1. names in all UPPERCASE_LETTERS, which is a common convention
           2. variables that were declared to be constant by the inclusion
              of a "Final" type hint.

        Note: We only override methods which could result in changing the value
        of a constant.
    """

    def __init__(self, module_filename):
        """Initialises the instance"""
        self.__file__ = module_filename
        super().__init__()

    def __setitem__(self, key, value):
        """Sets self[key] to value.

           If key is identified as a constant, it prevents changing
           its value after initial assignment.
        """
        if key in CONSTANTS[self.__file__]:
            print(
                "You cannot change the value of %s.%s to %s."
                % (shorten_path(self.__file__), key, value)
            )
            return
        if key == key.upper() or key in DECLARED_FINAL[self.__file__]:
            CONSTANTS[self.__file__][key] = value
        return super().__setitem__(key, value)

    def __delitem__(self, key):
        """Deletes self[key] unless key is identified as a constant"""
        if key in CONSTANTS[self.__file__]:
            print(
                "You cannot delete %s in module %s."
                % (key, shorten_path(self.__file__))
            )
            return
        return super().__delitem__(key)

    def setdefault(self, key, default=None):
        """Insert key with a value of default if key is not in the dictionary.

           Prevents changes if the key is identified as a constant.
        """
        if key in CONSTANTS[self.__file__]:
            print(
                "You cannot change the value of %s.%s."
                % (shorten_path(self.__file__), key)
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
            print(
                "You cannot delete %s in module %s."
                % (key, shorten_path(self.__file__))
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

       Pattern we are looking for::
           python_identifier : Final ...
    """
    CONSTANTS[filename] = {}
    DECLARED_FINAL[filename] = set([])

    for line in utils.get_lines_of_tokens(source):
        if (
            len(line) >= 4
            and line[0].is_identifier()
            and line[1].is_operator(":")
            and line[2].string == "Final"
        ):
            DECLARED_FINAL[filename].add(line[0].string)
    return source


def add_hook():
    """Creates and adds the import hook in sys.meta_path"""
    hook = import_hook.create_hook(
        module_class=ModuleWithConstants,
        source_transformer=transform_source,
        module_dict=FinalDict,
    )
    sys.meta_path.insert(0, hook)
    return hook


def remove_hook(hook):  # for testing
    """Useful for testing and isolating import hooks"""
    import_hook.remove_hook(hook)
