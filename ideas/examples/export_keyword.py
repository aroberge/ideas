"""
Export as a soft keyword
========================

More to come.


.. warning::

    Do not use continuation characters. The current transformation might not handle
    them correctly.

    A line that startswith an export statement may not contain a triple quoted string
    that spans multiple lines.

    A decorated class or function cannot be "exported"


"""

import sys
from ideas.utils import get_significant_tokens
import token_utils

# A better programmer would likely have written a recursive descent parser,
# or something similar, to process the source, extract the relevant information
# to make the appropriate change.
#
# what I did instead is to proceed in two parts, going through the entire source once
# and extracting the relevant information, before going through the entire source
# a second time to make the appropriate changes.
#
# When I have more time, I plan to add comments below to explain
# the reasoning behind this code.


class ExportInfo:
    def __init__(self, source):
        self.source = source
        self.export_statements_info = []
        self.indentation = 0
        self.current_row = -1
        self.inside_class_or_def = []
        self.open_brackets = []  # Any ([{ open but not closed
        self.class_or_def_indent = -1
        self.prev_token = None
        self.reset_flags()

    def reset_flags(self):
        self.begin_export = False
        self.export_class_or_def_name = False
        self.export_identifier = False
        self.export_stmt_info = {}

    def get_info(self):
        for self.token in get_significant_tokens(self.source):

            if not self.begin_export:
                if self.skip_over_irrelevant_token():
                    self.prev_token = self.token
                    continue

            if self.token.start_row > self.current_row and self.token == "export":
                self.init_export_statement()
                self.current_row = self.token.start_row
                self.prev_token = self.token
                continue

            if self.token.start_row > self.current_row:
                self.begin_new_statement()
                self.current_row = self.token.start_row
                self.prev_token = self.token
                continue

            if not self.begin_export:
                self.prev_token = self.token
                continue

            self.process_until_name_found()
            self.prev_token = self.token

        return self.export_statements_info

    def skip_over_irrelevant_token(self):
        if self.token.string in "([{":
            self.open_brackets.append(self.token.string)
            return True
        elif self.token.string in ")]}":
            self.open_brackets.pop()
            return True
        elif self.open_brackets:
            return True

        # if self.token.string in ["class", "def"]:
        #     self.inside_class_or_def.append(self.token)
        #     self.class_or_def_indent = self.token.start_col
        #     return True

        # if self.inside_class_or_def:
        #     if self.token.start_col > self.class_or_def_indent:
        #         return True
        #     while self.inside_class_or_def:
        #         prev_class_or_def = self.inside_class_or_def.pop()
        #         self.class_or_def_indent = prev_class_or_def.start_col
        #         if self.token.start_col > self.class_or_def_indent:
        #             return True

        return False

    def init_export_statement(self):
        """Initialize relevant variables when a new potentially valid export
        statement is found.
        """
        self.reset_flags()
        self.begin_export = True
        self.current_row = self.token.start_row
        self.indentation = self.token.start_col
        self.export_stmt_info = {
            "indentation": self.indentation * " ",
            "row": self.current_row,
            "name": "",
            "export token": self.token,
        }

    def begin_new_statement(self):
        self.reset_flags()
        self.current_row = self.token.start_row

    def process_until_name_found(self):
        """Identify name to be exported"""
        if (
            self.token == "def" or self.token == "class"
        ) and self.prev_token == "export":
            self.export_class_or_def_name = True
            return
        if self.token == "def" or self.token == "class":  # should never happen
            self.reset_flags()
            return

        if (
            self.prev_token == "def" or self.prev_token == "class"
        ) and self.token.is_identifier():
            self.export_stmt_info["name"] = self.token.string
            self.export_statements_info.append(self.export_stmt_info)
            self.reset_flags()
            return
        if (
            self.prev_token == "def" or self.prev_token == "class"
        ):  # should never happen
            self.reset_flags()
            return

        if (
            self.prev_token == "export"
            and self.token.is_identifier()
            and not self.export_identifier
        ):
            self.export_identifier = True
            return

        if not self.export_identifier:
            self.reset_flags()

        if self.prev_token == "export" and self.token.is_identifier():
            if not self.export_stmt_info["name"]:
                self.export_stmt_info["name"] = self.token.string
            # else, export is the (potential) identifier and we have "export export ..."
            return

        if self.token == "=":
            self.export_statements_info.append(self.export_stmt_info)
            self.reset_flags()
        return

    # def process_end_of_from_statement(self):
    #     """Identify public names after export keyword"""
    #     self.current_row = self.token.start_row
    #     if self.token.is_identifier():
    #         if self.prev_token == "as":
    #             self.export_stmt_info["public names"].pop()
    #         self.export_stmt_info["public names"].append(self.token.string)
    #     elif self.token == "(":
    #         self.open_parens.append(self.token)
    #     elif self.token == ")":
    #         self.open_parens.pop()
    #         if not self.open_parens:  # this should be the case
    #             self.export_stmt_info["next row"] = self.current_row + 1
    #     elif self.token == "*":
    #         self.export_stmt_info["public names"] = "*"


def _display_location(info):
    """used for doing quick test at the terminal or debugging tests"""
    print(f"{len(info)=}")
    for entry in info:
        for item in entry:
            if item == "indentation":
                print(item, f"|{entry[item]}|")
            else:
                print(item, repr(entry[item]))
        print()


def insert_all_info(new_tokens, current_info):

    new_all = """
{indent}__all__ = globals().setdefault("__all__", [])
{indent}__all__ = list(__all__)
{indent}__all__.append({name})
"""
    new_tokens.append(
        new_all.format(
            indent=current_info["indentation"],
            name=current_info["name"],
        )
    )
    return new_tokens


def transform_source(source, **kwargs):
    new_tokens = []

    info_locator = ExportInfo(source)
    info = info_locator.get_info()
    # _display_location(info)

    current_info = None
    prev_token = None

    if info:
        current_info = info.pop(0)

    for token in token_utils.tokenize(source):
        if prev_token is not None:
            prev_token.string = token.string
            token.string = "      "  # length of export
            new_tokens.append(prev_token)
            new_tokens.append(token)
            prev_token = None
            continue

        if current_info is not None and token.is_identical(
            current_info["export token"]
        ):
            same_line_tokens = []
            while new_tokens:
                tok = new_tokens.pop()
                if tok.start_row == token.start_row:
                    same_line_tokens.append(tok)
                else:
                    new_tokens.append(tok)
                    break
            new_tokens = insert_all_info(new_tokens, current_info)
            new_tokens.extend(same_line_tokens)
            prev_token = token
            continue

        new_tokens.append(token)
    new_source = token_utils.untokenize(new_tokens)

    if "pytest" in sys.modules:
        if source != new_source:
            print("\n====== Original source for export keyword ============")
            print(source)
            print("-----------------")
            print("\n====== New source ============")
            print(new_source)
            print("-----------------")
        else:
            print("No change in source")
    return new_source


def add_hook():
    from ideas import create_hook

    return create_hook(transform_source=transform_source, name=__name__)
