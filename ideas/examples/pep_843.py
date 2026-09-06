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

For simplicity, we will only consider cases where ``__all__``
is a list, and not a tuple as preferred by some programmers.
This will allow us to simplify the above to::

    from <module> import <name> as <alias>
    __all__ = globals().setdefault("__all__", [])
    __all__.append("<alias>")

PEP 843 also states that
*unlike ``import``, ``export`` is restricted to module level:
it’s a ``SyntaxError`` inside a ``def`` or ``class`` body.*

As such, we will not transform "export" if it occurs within
a class or function body.
"""

import token_utils
import tokenize as py_tokenize
from io import StringIO


def is_identical(self, other):
    return repr(self) == repr(other)


token_utils.Token.is_identical = is_identical


class ExportInfo:
    def __init__(self, source):
        self.source = source
        self.from_statements_info = []
        self.indentation = 0
        self.current_row = -1
        self.begin_from = False

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
            if self.token == "from":
                self.init_from_statement()
                continue

            if self.token.start_row > self.current_row:
                self.begin_new_statement()
                continue

            if not self.begin_from:
                self.prev_token = self.token
                continue

            if not self.export_found:
                self.process_until_export_statement()
                continue

            self.process_end_of_from_statement()

        # if from statement was last statement of source, we need to add it.
        if self.from_stmt_info:
            self.from_statements_info.append(self.from_stmt_info)
        return self.from_statements_info

    def init_from_statement(self):
        """Initialize relevant variables when a new from statement is found."""
        if self.begin_from:
            self.from_statements_info.append(self.from_stmt_info)
        self.begin_from = True
        self.current_row = self.token.start_row
        self.indentation = self.token.start_col
        self.from_stmt_info = {
            "indentation": self.indentation * " ",
            "row": self.current_row,
            "next row": self.current_row + 1,
            "public names": [],
            "module name": [],
            "export token": None,
        }
        self.prev_token = self.token
        self.export_found = False

    def begin_new_statement(self):
        if self.begin_from:
            self.from_statements_info.append(self.from_stmt_info)
            self.from_stmt_info = {}
        self.current_row = self.token.start_row
        self.prev_token = self.token

    def process_until_export_statement(self):
        """Identify module name and if export/import is used"""
        if self.token == "import":  # drop everything for this line
            self.begin_from = False
            self.from_stmt_info = {}
            self.prev_token = self.token
            return

        elif self.token == "export":
            self.export_found = True
            self.from_stmt_info["export token"] = self.token
            self.prev_token = self.token
            return

        self.from_stmt_info["module name"].append(self.token.string)
        return

    def process_end_of_from_statement(self):
        """Identify public names after export keyword"""
        if self.token.is_identifier():
            if self.prev_token == "as":
                self.from_stmt_info["public names"].pop()
            self.from_stmt_info["public names"].append(self.token.string)
        self.prev_token = self.token


# def display_location(info):
#     """used for doing quick test at the terminal"""

#     for entry in info:
#         for item in entry:
#             if item == "indentation":
#                 print(item, f"|{entry[item]}|")
#             else:
#                 print(item, entry[item])
#         print()


def transform_source(source, **kwargs):
    new_tokens = []
    new_all = '\n{}__all__ = globals().setdefault("__all__", {})'
    all_append = "\n{}__all__.extend({})\n"

    info_locator = ExportInfo(source)
    info = info_locator.get_info()
    # display_location(info)

    current_info = None

    if info:
        current_info = info.pop(0)

    for tokens in token_utils.get_lines(source):
        for token in tokens:
            if current_info is not None:
                if token.is_identical(current_info["export token"]):
                    token.string = "import"
                    new_tokens.append(token)
                    continue

                if token.start_row == current_info["next row"]:
                    if new_tokens[-1] == "\n":
                        new_tokens.pop()
                    new_tokens.append(
                        new_all.format(
                            current_info["indentation"], current_info["public names"]
                        )
                    )
                    new_tokens.append(
                        all_append.format(
                            current_info["indentation"], current_info["public names"]
                        )
                    )
                    if info:
                        current_info = info.pop(0)
                    else:
                        current_info = None
            new_tokens.append(token)

    if current_info is not None:
        new_tokens.append(
            new_all.format(current_info["indentation"], current_info["public names"])
        )
        new_tokens.append(
            all_append.format(current_info["indentation"], current_info["public names"])
        )
    new_source = token_utils.untokenize(new_tokens)
    # print("======New source")
    # print(new_source)
    # print("-----------------")
    return new_source


def add_hook():
    from ideas import create_hook  # noqa

    pass
