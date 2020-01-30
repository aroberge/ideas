"""utils.py

A few useful objects which do not naturally fit anywhere else.
"""
import keyword
import tokenize
import os.path

from io import StringIO

_token_format = "type={type}  string={string}  start={start}  end={end}  line='{line}'"


class Token:
    """Token as generated from tokenize.generate_tokens written here in
       a more convenient form for our purpose. The various
       paramters are::

           type: token type
           string: the token written as a string
           start = (start_row, start_col)
           end = (end_row, end_col)
           line: entire line of code where the token is found.
    """

    def __init__(self, token):
        self.type = token[0]
        self.string = token[1]
        self.start = self.start_row, self.start_col = token[2]
        self.end = self.end_row, self.end_col = token[3]
        self.line = token[4]
        if self.line and self.line[-1] == "\n":
            self.line = self.line[:-1]

    def is_keyword(self, name=None):
        """Returns True if the token represents a Python keyword.

           If ``name`` is specified, then it returns True only if
           the keyword is the one specified.
        """
        if name is not None:
            return (
                self.type == tokenize.NAME
                and keyword.iskeyword(self.string)
                and name == self.string
            )
        else:
            return self.type == tokenize.NAME and keyword.iskeyword(self.string)

    def is_identifier(self):
        """Returns True if the token is a Python identifier"""
        return self.type == tokenize.NAME and self.string.isidentifier()

    def is_operator(self, operator=None):
        """Returns True if the token is a Python operator and if operator is
            equal to the default value (None).

            If a string representing the operator is specified, this function
            will return True only if the token is this specific operator.
        """
        if operator is None:
            return self.type == tokenize.OP
        else:
            return self.type == tokenize.OP and self.string == operator

    def __repr__(self):
        """Nicely formatted token"""
        return _token_format.format(
            type="%s (%s)" % (self.type, tokenize.tok_name[self.type]),
            string=repr(self.string),
            start=str(self.start),
            end=str(self.end),
            line=str(self.line).replace("\t", "\\t"),
        )


def tokenize_source(source, ignore_spaces=False, ignore_comments=False):
    """Makes a list of tokens from a source (str), with the option of
       ignoring comments and/or spaces."""
    tokens = []
    # empty_NL_token = False
    try:
        for tok in tokenize.generate_tokens(StringIO(source).readline):
            token = Token(tok)
            if ignore_comments and token.type == tokenize.COMMENT:
                continue
            if ignore_spaces and not token.string.strip():
                continue

            # Todo: see if https://bugs.python.org/issue35107#msg328884 is ok
            tokens.append(token)

    except (tokenize.TokenError, Exception) as exc:
        print("###\nWARNING: the following tokenize error was raised\n", exc, "\n###")

    return tokens


def get_lines_of_tokens(source):
    """Makes a list of lists of tokens, with each (inner) list including
       all tokens that start on the same line"""
    lines = []
    current_line = -1
    new_line = []
    try:
        for tok in tokenize.generate_tokens(StringIO(source).readline):
            token = Token(tok)
            if token.type == tokenize.COMMENT:
                continue
            if not token.string.strip():  # ignore spaces
                continue
            if token.start_row != current_line:
                current_line = token.start_row
                if new_line:
                    lines.append(new_line)
                new_line = []
            new_line.append(token)
    except (tokenize.TokenError, Exception) as exc:
        print("###\nWARNING: the following tokenize error was raised\n", exc, "\n###")

    if new_line:
        lines.append(new_line)
    return lines


# untokenize adapted from https://github.com/myint/untokenize
#
# TODO: acknowledge it properly in documentation with license added
#


TOKENIZE_HAS_ENCODING = hasattr(tokenize, "ENCODING")
WHITESPACE_TOKENS = (tokenize.INDENT, tokenize.NEWLINE, tokenize.NL)


def untokenize(tokens):
    """Return source code based on tokens.

    This is similar to tokenize.untokenize(), but it preserves spacing between
    tokens. So if the original soure code had multiple spaces between
    some tokens or if escaped newlines were used, those things will be
    reflected by untokenize().

    Adapted from https://github.com/myint/untokenize
    """
    words = []
    previous_line = ""
    last_row = 0
    last_column = -1
    last_non_whitespace_tokey_type = None

    for token in tokens:
        if TOKENIZE_HAS_ENCODING and token.type == tokenize.ENCODING:
            continue

        # Preserve escaped newlines.
        if (
            last_non_whitespace_tokey_type != tokenize.COMMENT
            and token.start_row > last_row
        ):
            if previous_line.endswith(("\\\n", "\\\r\n", "\\\r")):  # original
                words.append(previous_line[len(previous_line.rstrip(" \t\n\r\\")) :])
            elif previous_line.endswith("\\"):  # my fix
                words.append(previous_line[len(previous_line.rstrip(" \t\\")) :])
                words.append("\n")

        # Preserve spacing.
        if token.start_row > last_row:
            last_column = 0
        if token.start_col > last_column:
            words.append(token.line[last_column : token.start_col])

        words.append(token.string)

        previous_line = token.line

        last_row = token.end_row
        last_column = token.end_col

        if token.type not in WHITESPACE_TOKENS:
            last_non_whitespace_tokey_type = token.type

    return "".join(words)


PYTHON = os.path.dirname(os.__file__).lower()
this_dir = os.path.dirname(__file__)
IDEAS = os.path.abspath(os.path.join(this_dir, "..")).lower()
TESTS = os.path.join(IDEAS, "tests").lower()
HOME = os.path.expanduser("~").lower()


def shorten_path(path):
    """Utility function used to reduce the length of the path shown
       to a user. For example, a path for a module in the Python
       standard library might be shown as::

           PYTHON:/module.py

       whereas a file found in the user's root directory might be shown
       as::

            ~/dir/file.py
    """
    # On windows, the filenames are not case sensitive
    # and the way Python displays filenames may vary.
    # To properly compare, we convert everything to lowercase
    # However, we ensure that the shortened path retains its cases
    path_lower = path.lower()
    if path_lower.startswith(TESTS):
        path = "TESTS:" + path[len(TESTS) :]
    elif path_lower.startswith(IDEAS):
        path = "IDEAS:" + path[len(IDEAS) :]
    elif path_lower.startswith(PYTHON):
        path = "PYTHON:" + path[len(PYTHON) :]
    elif path_lower.startswith(HOME):
        path = "~" + path[len(HOME) :]
    return path


def print_tokens(source):
    """Prints tokens found in source, excluding spaces and comments.

       This is occasionally useful to use at the console during development.
    """
    tokens = tokenize_source(source)
    for token in tokens:
        print(token)
