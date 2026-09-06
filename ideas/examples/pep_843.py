"""

PEP 843
=======

PEP 843 suggests the addition of ``export`` as a soft keyword to be
used in expressions of the basic form::

    from x export y [as z]

with other slight variations described below. Assuming that
``__all__ = [...]`` is already defined, the statement

.. code-block::

    from x export y

would be equivalent to

.. code-block::

    from x import y
    __all__.append(y)

Implementation
--------------

We implement this as a source transformation. PEP 843 suggests that::

    from <module> import <name> as <alias>

should be equivalent to::

    from <module> import <name> as <alias>
    exported_names = globals().setdefault("__all__", [])
    if not isinstance(exported_names, list):
        exported_names = list(exported_names)
        __all__ = exported_names
    exported_names.append("<alias>")

We avoid introducing ``exported_names`` as an intermediary
variable by doing something like the following instead::

    from <module> import <name> as <alias>
    __all__ = globals().setdefault("__all__", [])
    __all__ = list(__all__)
    __all__.extend(["<alias>"])

PEP 843 also states that
*unlike ``import``, ``export`` is restricted to module level:
it’s a ``SyntaxError`` inside a ``def`` or ``class`` body.*

As such, we will **not** transform "export" if it occurs within
a class or function body.

Star version
-----------

For the star version::

    from module export *

we believe that the following should do what is expected::

    from module import *
    __all__ = globals().setdefault("__all__", [])
    __all__ = list(__all__)
    if hasattr(module, "__all__"):
        __all__.extend(list(module.__all__))
    else:
        for _ in dir(module):
            if not _.startswith("_"):
                __all__.append(_)
"""

import token_utils
import tokenize as py_tokenize
from io import StringIO
import sys


def is_identical(self, other):
    return repr(self) == repr(other)


token_utils.Token.is_identical = is_identical


class ExportInfo:
    def __init__(self, source):
        self.source = source
        self.from_statements_info = []
        self.from_stmt_info = {}
        self.indentation = 0
        self.current_row = -1
        self.begin_from = False
        self.inside_class_or_def = []
        self.open_brackets = []  # Any ([{ open but not closed
        self.class_or_def_indent = -1
        self.prev_token = None
        self.open_parens = []  # inside from ... import (...)

    def get_significant_tokens(self):
        """Gets a list of tokens from a source (str), ignoring comments
        as well as any token whose string value is either null or
        consists of spaces, newline or tab characters.

        If an exception is raised by Python's tokenize module, the list of tokens
        accumulated up to that point is returned.
        """
        for tok in py_tokenize.generate_tokens(StringIO(self.source).readline):
            token = token_utils.Token(tok)
            if not token.string.strip():
                continue
            if token.is_comment():
                continue
            yield token

    def get_info(self):
        for self.token in self.get_significant_tokens():

            if not self.begin_from:
                if self.skip_over_irrelevant_token():
                    self.prev_token = self.token
                    continue

            if self.token == "from":
                self.init_from_statement()
                self.prev_token = self.token
                continue

            if self.token.start_row > self.current_row and not self.open_parens:
                self.begin_new_statement()
                self.prev_token = self.token
                continue

            if not self.begin_from:
                self.prev_token = self.token
                continue

            if not self.export_found:
                self.process_until_export_statement()
                self.prev_token = self.token
                continue

            self.process_end_of_from_statement()
            self.prev_token = self.token

        # if from statement was last statement of source, we need to add it.
        if self.from_stmt_info:
            self.from_statements_info.append(self.from_stmt_info)
        return self.from_statements_info

    def skip_over_irrelevant_token(self):
        if self.token.string in "([{":
            self.open_brackets.append(self.token.string)
            return True
        elif self.token.string in ")]}":
            self.open_brackets.pop()
            return True
        elif self.open_brackets:
            return True

        if self.token.string in ["class", "def"]:
            self.inside_class_or_def.append(self.token)
            self.class_or_def_indent = self.token.start_col
            return True

        if self.inside_class_or_def:
            if self.token.start_col > self.class_or_def_indent:
                return True
            while self.inside_class_or_def:
                prev_class_or_def = self.inside_class_or_def.pop()
                self.class_or_def_indent = prev_class_or_def.start_col
                if self.token.start_col > self.class_or_def_indent:
                    return True

        return False

    def init_from_statement(self):
        """Initialize relevant variables when a new from statement is found."""
        if self.begin_from:
            self.from_statements_info.append(self.from_stmt_info)
        self.begin_from = True
        self.current_row = self.token.start_row
        self.indentation = self.token.start_col
        if self.prev_token == "lazy":
            self.indentation = self.prev_token.start_col
        self.from_stmt_info = {
            "indentation": self.indentation * " ",
            "row": self.current_row,
            "next row": self.current_row + 1,
            "public names": [],
            "module name": "",
            "export token": None,
        }
        self.export_found = False

    def begin_new_statement(self):
        if self.begin_from:
            self.from_statements_info.append(self.from_stmt_info)
            self.from_stmt_info = {}
        self.current_row = self.token.start_row

    def process_until_export_statement(self):
        """Identify module name and if export/import is used"""
        if self.token == "import":  # drop everything for this line
            self.begin_from = False
            self.from_stmt_info = {}
            return

        elif self.token == "export":
            self.export_found = True
            self.from_stmt_info["export token"] = self.token
            return

        self.from_stmt_info["module name"] += self.token.string
        return

    def process_end_of_from_statement(self):
        """Identify public names after export keyword"""
        self.current_row = self.token.start_row
        if self.token.is_identifier():
            if self.prev_token == "as":
                self.from_stmt_info["public names"].pop()
            self.from_stmt_info["public names"].append(self.token.string)
        elif self.token == "(":
            self.open_parens.append(self.token)
        elif self.token == ")":
            self.open_parens.pop()
            if not self.open_parens:  # this should be the case
                self.from_stmt_info["next row"] = self.current_row + 1
        elif self.token == "*":
            self.from_stmt_info["public names"] = "*"


def display_location(info):
    """used for doing quick test at the terminal"""

    for entry in info:
        for item in entry:
            if item == "indentation":
                print(item, f"|{entry[item]}|")
            elif item == "export token":
                print(item, repr(entry[item]))
            else:
                print(item, entry[item])
        print()


def insert_all_info(new_tokens, current_info):

    new_all = """
{indent}__all__ = globals().setdefault("__all__", [])
{indent}__all__ = list(__all__)
{indent}__all__.extend({names})
"""

    new_all_star = """
{indent}__all__ = globals().setdefault("__all__", [])
{indent}__all__ = list(__all__)
{indent}if hasattr({module}, "__all__"):
{indent}    __all__.extend(list({module}.__all__))
{indent}else:
{indent}    for _ in dir({module}):
{indent}        if not _.startswith("_"):
{indent}            __all__.append(_)
"""

    if current_info["public names"] == "*":
        new_tokens.append(
            new_all_star.format(
                indent=current_info["indentation"],
                module=current_info["module name"],
            )
        )
    else:
        new_tokens.append(
            new_all.format(
                indent=current_info["indentation"],
                names=current_info["public names"],
            )
        )

    return new_tokens


def transform_source(source, **kwargs):
    new_tokens = []

    info_locator = ExportInfo(source)
    info = info_locator.get_info()
    display_location(info)

    current_info = None

    if info:
        current_info = info.pop(0)

    if "pytest" in sys.modules:
        print("\n====== Original source for pep_843 ============")
        print(source)
        print("-----------------")

    for tokens in token_utils.get_lines(source):

        for token in tokens:
            if current_info is None or current_info["row"] > token.start_row:
                new_tokens.append(token)
                continue

            if token.is_identical(current_info["export token"]):
                token.string = "import"
                new_tokens.append(token)
                continue

            if token.start_row == current_info["next row"]:
                if new_tokens[-1] == "\n":
                    new_tokens.pop()
                new_tokens = insert_all_info(new_tokens, current_info)
                if info:
                    current_info = info.pop(0)
                else:
                    current_info = None
            new_tokens.append(token)

    if current_info is not None:
        new_tokens = insert_all_info(new_tokens, current_info)
    new_source = token_utils.untokenize(new_tokens)

    if "pytest" in sys.modules:
        print("\n====== New source ============")
        print(new_source)
        print("-----------------")
    return new_source


def add_hook():
    from ideas import create_hook  # noqa

    pass
