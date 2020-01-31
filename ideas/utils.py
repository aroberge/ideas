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

    def is_comment(self):
        """Returns True if the token is a comment"""
        return self.type == tokenize.COMMENT

    def __repr__(self):
        """Nicely formatted token"""
        return _token_format.format(
            type="%s (%s)" % (self.type, tokenize.tok_name[self.type]),
            string=repr(self.string),
            start=str(self.start),
            end=str(self.end),
            line=str(self.line).replace("\t", "\\t"),
        )


def tokenize_source(source):
    """Makes a list of tokens from a source (str)."""
    tokens = []

    try:
        for tok in tokenize.generate_tokens(StringIO(source).readline):
            token = Token(tok)
            tokens.append(token)
    except (tokenize.TokenError, Exception) as exc:
        print("WARNING: the following error was raised in tokenize_source\n", exc)

    return tokens


def get_lines_of_tokens(source):
    """Makes a list of lists of tokens, with each (inner) list either
       all the DEDENT tokens found on a single line,
       or all the other tokens found on a single line.

       The separate treatement of DEDENT tokens is to make it easier
       to process the content.
    """
    lines = []
    current_line = -1
    new_line = []
    new_dedent_line = []
    try:
        for tok in tokenize.generate_tokens(StringIO(source).readline):
            token = Token(tok)
            if token.start_row != current_line:
                current_line = token.start_row
                if new_dedent_line:
                    lines.append(new_dedent_line)
                if new_line:
                    lines.append(new_line)
                new_dedent_line = []
                new_line = []
            if token.type == tokenize.DEDENT:
                new_dedent_line.append(token)
            else:
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

WHITESPACE_TOKENS = (tokenize.INDENT, tokenize.NEWLINE, tokenize.NL)


def untokenize(tokens):
    """Return source code based on tokens.

    This is similar to Python's tokenize.untokenize(), except that it
    preserves spacing between tokens, by using the ``line``
    information recorded by Python's ``tokenize.generate_tokens``.
    As a result, if the original soure code had multiple spaces between
    some tokens or if escaped newlines were used, those things will be
    reflected by ``untokenize``.

    However, if some tokens are changed, the ``line`` information will
    no longer reflect the content and the reconstructed content may
    no longer be valid, unless some special procedures have been followed
    when replacing original tokens by new ones. See the documentation
    for examples.

    Adapted from https://github.com/myint/untokenize
    """
    words = []
    previous_line = ""
    last_row = 0
    last_column = -1
    last_non_whitespace_tokey_type = None

    for token in tokens:
        if token.type == tokenize.ENCODING:
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


INVALID_TOKEN_MESSAGE = """Invalid token in simple_untokenize.

A valid token can be either an object having both a 'type' and a 'string'
attribute, or a an iterable with of length 2 like
(type, string).

The token that raised this error was:
%s
"""


def simple_untokenize(tokens):  # untested
    """Reconstructs a source from a list of tokens. Each token can be
    either an instance of the Token class, or a tuple consisting
    of two values: the token type and the token string.

    Generates a string correspondings to a list of tokens based only
    on the token type and string information. This does not preserve
    the spacing between tokens which was present in the original source.
    """
    simple_tokens = []
    for token in tokens:
        if hasattr(token, "type"):
            if token.type == tokenize.ENCODING:
                continue
        if hasattr(token, "type") and hasattr(token, "string"):
            token = (token.type, token.string)
        elif len(token) != 2:
            raise TypeError(INVALID_TOKEN_MESSAGE % str(token))
        simple_tokens.append(token)

    return tokenize.untokenize(simple_tokens)


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
    current = os.getcwd()

    if path_lower.startswith(PYTHON):
        path = "PYTHON:" + path[len(PYTHON) :]
    elif path_lower.startswith(IDEAS):
        path = "IDEAS:" + path[len(IDEAS) :]
    elif path_lower.startswith(current):
        path = "CURRENT:" + path[len(current) :]
    elif path_lower.startswith(TESTS):
        path = "TESTS:" + path[len(TESTS) :]
    elif path_lower.startswith(HOME):
        path = "~" + path[len(HOME) :]
    return path


def print_paths():
    """Prints the values of the path abbreviations used in shorten_path()."""
    print(f"~: {HOME}")
    print(f"CURRENT: {os.getcwd()}")
    print(f"PYTHON: {PYTHON}")
    print(f"IDEAS: {IDEAS}")
    if os.path.exists(TESTS):
        print(f"TESTS: {TESTS}")


def print_tokens(source):
    """Prints tokens found in source, excluding spaces and comments.

       Source is either a string to be tokenized, or a list of tokens.

       This is occasionally useful as a debugging tool.
    """
    if isinstance(source[0], Token):
        tokens = source
    else:
        tokens = tokenize_source(source)
    for token in tokens:
        print(token)
