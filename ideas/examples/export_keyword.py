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
        self.export_variable = False
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

            # Restrict "export identifier ... = " to be on a single line.
            if self.token.start_row > self.current_row:
                self.begin_new_statement()
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
        if self.token == "export":
            self.begin_export = True

    def process_until_name_found(self):
        """Identify name to be exported"""
        if (
            self.token == "def" or self.token == "class"
        ) and self.prev_token == "export":
            self.export_class_or_def_name = True
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
        ) and not self.token.is_identifier():
            self.reset_flags()
            return

        # Next, it's finding a variable name
        if (
            self.prev_token == "export"
            and self.token.is_identifier()
            and not self.export_variable
        ):
            self.export_variable = True
            if not self.export_stmt_info["name"]:
                # else, export is the (potential) identifier and we have "export export ..."
                self.export_stmt_info["name"] = str(self.token.string)
                # this token string needs to be converted as it will be altered later
            return

        if not self.export_variable:  # should not happen ... just to be safe ..
            self.reset_flags()

        if self.token == "=" and self.export_variable:
            self.export_statements_info.append(self.export_stmt_info)
            self.reset_flags()
        return

    def find_def_or_class_name(self):
        pass


def _display_location(info):
    """used for doing quick test at the terminal or debugging tests"""
    print(f"{len(info)=}")
    for entry in info:
        for item in entry:
            if item == "indentation":
                print(item, f"|{entry[item]}|")
            else:
                print(item, repr(entry[item]))
    print("-------------------")


def insert_all_info(new_tokens, current_info):

    new_all = """
{indent}__all__ = globals().setdefault("__all__", [])
{indent}__all__ = list(__all__)
{indent}__all__.append('{name}')
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
    _display_location(info)

    current_line = -1
    current_info = None
    prev_token = None
    changes_should_be_made = False

    if info:
        changes_should_be_made = True
        current_info = info.pop(0)  # important: need to pop from the beginning

    for token in token_utils.tokenize(source):
        if prev_token is None:
            new_tokens.append(token)
            prev_token = token
            continue

        if current_line != token.start_row:
            current_line = token.start_row

        if not current_info:  # we are done
            new_tokens.append(token)
            continue

        if current_info and prev_token.is_identical(current_info["export token"]):
            same_line_tokens = []
            while new_tokens:
                tok = new_tokens.pop()
                if tok.start_row == token.start_row:
                    if tok.is_identical(current_info["export token"]):
                        tok.string = token.string  # change export name
                    same_line_tokens.insert(0, tok)
                else:
                    new_tokens.append(tok)
                    break

            new_tokens = insert_all_info(new_tokens, current_info)
            new_tokens.extend(same_line_tokens)
            token.string = "      "  # length of export
            new_tokens.append(token)
            prev_token = token
            if info:
                current_info = info.pop(0)  # important: need to pop from the beginning
            else:
                current_info = None
            continue

        new_tokens.append(token)
        prev_token = token

    new_source = token_utils.untokenize(new_tokens)

    if changes_should_be_made:
        if new_source == source:
            print(
                "PROBLEM: changes to the source should have been made since 'info' is not empty!"
            )
    return new_source


def add_hook(**_kwargs):
    from ideas import create_hook

    return create_hook(transform_source=transform_source, name=__name__)
