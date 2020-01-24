import re
import sys
import types

from ideas import import_hook

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
    def __setattr__(self, attr, value, final=False):
        if self.__file__ not in CONSTANTS:
            CONSTANTS[self.__file__] = {}

        if attr in CONSTANTS[self.__file__]:
            print(
                "You cannot change the value of %s.%s to %s"
                % (self.__name__, attr, value)
            )
            return

        if (
            final  # from optional type declaration
            or attr == attr.upper()  # Python convention for constant names
        ):
            CONSTANTS[self.__file__][attr] = value

        super().__setattr__(attr, value)

    def __delattr__(self, attr):
        if self.__file__ not in CONSTANTS:
            CONSTANTS[self.__file__] = {}

        if attr in CONSTANTS[self.__file__]:
            print(
                "You cannot delete the constant %s of module %s"
                % (attr, self.__name__)
            )
            return

        super().__delattr__(attr)


# For this example, we use simple regular expressions to identify
# lines of code that correspond to variable assignments. It is assumed
# that each assignment is done on a single line of code.
# This approach can change values within triple-quoted strings
# and does not capture all the possible cases for variable assignments.
# It is simply used as a quick demonstration.


# A basic assignement pattern we look for is something like
#     python_identifier = whatever
# which can be an indented statement.
assignment_pattern = re.compile(r"^\s*([\w][\w\d]*)\s*=\s*(.+)")
# Note that the regex used for Python identifiers might not cover all
# possible valid identifiers with non-ascii characters.

# We also include something like
#     python_identifier : Final = whatever
# but assume that it would not be indented.
final_declaration_pattern = re.compile(r"^([\w][\w\d]*)\s*:\s*Final\s*=\s*(.+)")


def transform_source(source):
    """Identifies simple assignments, including those with a Final type
       hint, and replace them by a special function call.

       So, something like

           name = value

       gets replaced by something like

           sys.modules[__name__].__setattr__(name, value)
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
    new_lines = ["import sys as %s" % sys_name]
    for line in lines:
        match = re.search(assignment_pattern, line)
        match_final = re.search(final_declaration_pattern, line)
        if match:
            name = match.group(1)
            indent = len(line) - len(line.lstrip())
            value = match.group(2)
            new_lines.append(
                " " * indent
                + "%s.modules[__name__].__setattr__(" % sys_name
                + "'%s', (%s))" % (name, value)
            )
        elif match_final:
            name = match_final.group(1)
            value = match_final.group(2)
            new_lines.append(
                "%s.modules[__name__].__setattr__(" % sys_name
                + "'%s', (%s), final=True)" % (name, value)
            )
        else:
            new_lines.append(line)

    return "\n".join(new_lines)


def add_hook():
    hook = import_hook.create_hook(module_class=ModuleWithConstants,
                                   source_transformer=transform_source)
    sys.meta_path.insert(0, hook)
    return hook


def remove_hook(hook):
    import_hook.remove_hook(hook)
