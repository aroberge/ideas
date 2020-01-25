import re
import sys
import types

from ideas import import_hook

shorten_path = import_hook.shorten_path
CONSTANTS = {}


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
        if self.__file__ not in CONSTANTS:
            CONSTANTS[self.__file__] = {}

        if attr in CONSTANTS[self.__file__]:
            print(
                "You cannot change the value of %s.%s to %s"
                % (shorten_path(self.__file__), attr, value)
            )
            return
        if attr == attr.upper():
            print("You cannot add constants to another module.")
            return
        super().__setattr__(attr, value)

    def __delattr__(self, attr):
        if self.__file__ not in CONSTANTS:
            CONSTANTS[self.__file__] = {}

        if attr in CONSTANTS[self.__file__]:
            print(
                "You cannot delete the constant %s of module %s"
                % (attr, shorten_path(self.__file__))
            )
            return

        super().__delattr__(attr)


class FinalDict(dict):
    """dict subclass which ensures that constants are not over-written.

        Constants are identified in two ways:
           1. names in all UPPERCASE_LETTERS, which is a common convention
           2. variables that were declared to be constant by the inclusion
              of a "Final" type hint.

        We only override methods which could result in changing the value
        of a constant.
    """

    def __init__(self, module_filename):
        self.__file__ = module_filename
        if self.__file__ not in CONSTANTS:
            CONSTANTS[self.__file__] = {}
        super().__init__()

    def __setitem__(self, key, value):
        if key in CONSTANTS[self.__file__]:
            print(
                "You cannot change the value of %s.%s to %s."
                % (shorten_path(self.__file__), key, value)
            )
            return
        try:
            declared_final = self.__getitem__("__declared_final__")
        except Exception:
            declared_final = []
        if (
            key == key.upper() or key in declared_final
        ):  # Python convention for constants
            CONSTANTS[self.__file__][key] = value
        return super().__setitem__(key, value)

    def __delitem__(self, key):
        if key in CONSTANTS[self.__file__]:
            print(
                "You cannot delete %s in module %s."
                % (key, shorten_path(self.__file__))
            )
            return
        return super().__delitem__(key)

    def setdefault(self, key, default=None):
        if key in CONSTANTS[self.__file__]:
            print(
                "You cannot change the value of %s.%s."
                % (shorten_path(self.__file__), key)
            )
            return
        if key == key.upper():  # Python convention for constants
            CONSTANTS[self.__file__][key] = default
        return super().setdefault(key, default)

    def pop(self, key):
        if key in CONSTANTS[self.__file__]:
            print(
                "You cannot delete %s in module %s."
                % (key, shorten_path(self.__file__))
            )
            return CONSTANTS[self.__file__][key]
        return super().pop(key)

    def update(self, mapping_or_iterable=(), **kwargs):
        if hasattr(mapping_or_iterable, "keys"):
            for key in mapping_or_iterable:
                self.__setitem__(key, mapping_or_iterable[key])
        else:
            for key, value in mapping_or_iterable:
                self.__setitem__(key, value)

        for key in kwargs:
            self.__setitem__(key, kwargs[key])


# For this example, we use simple regular expressions to identify
# lines of code that correspond to variable assignments. It is assumed
# that each assignment is done on a single line of code.
# This approach can change values within triple-quoted strings
# and does not capture all the possible cases for variable assignments.
# It is simply used as a quick demonstration.

# We scan for lines that include something like
#     python_identifier : Final = whatever
# but assume that it would not be indented.
final_declaration_pattern = re.compile(r"^([\w][\w\d]*)\s*:\s*Final\s*=\s*(.+)")


def transform_source(source):
    """Identifies simple assignmentswith a Final type
       hint, adding a line of code which allows to keep track of them.

       So, something like

           name: Final = value

       gets replaced by something like

           __declared_final__.add('name')
           name = value
    """

    # We are going to add an import to Python's sys module and want to make
    # sure that it won't conflict with any variable in the source
    if "sys" not in source:
        sys_name = "sys"
    else:
        i = 0
        while True:
            sys_name = "sys" + str(i)
            if sys_name not in source:
                break
            i += 1

    lines = source.split("\n")
    new_lines = ["__declared_final__ = set([])"]
    for line in lines:
        match_final = re.search(final_declaration_pattern, line)
        if match_final:
            name = match_final.group(1)
            value = match_final.group(2)
            new_lines.append("__declared_final__.add('%s')" % name)
            new_lines.append("%s = %s" % (name, value))
        else:
            new_lines.append(line)

    return "\n".join(new_lines)


def add_hook():
    hook = import_hook.create_hook(
        module_class=ModuleWithConstants,
        source_transformer=transform_source,
        globals_=FinalDict,
    )
    sys.meta_path.insert(0, hook)
    return hook


def remove_hook(hook):  # for testing
    import_hook.remove_hook(hook)
