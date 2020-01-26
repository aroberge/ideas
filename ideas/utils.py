"""utils.py

A few useful objects which do not naturally fit anywhere else.
"""
import keyword
import token as token_module
import tokenize
import os.path

from io import StringIO

_token_format = "{type:<10}{string:<25} {start:^12} {end:^12} {line:^12}"


class Token:
    """Token as generated from tokenize.generate_tokens written here in
       a more convenient form for our purpose.
    """

    def __init__(self, token):
        self.type = token[0]
        self.string = token[1]
        self.start = self.start_line, self.start_col = token[2]
        self.end = self.end_line, self.end_col = token[3]
        self.line = token[4]
        if self.line and self.line[-1] == "\n":
            self.line = self.line[:-1]

    def is_keyword(self):
        """Returns True if the token represents a Python keyword"""
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
            type=token_module.tok_name[self.type],
            string=self.string,
            start=str(self.start),
            end=str(self.end),
            line=str(self.line),
        )


def tokenize_source(source):
    """Makes a list of tokens from a source (str), ignoring spaces and comments."""
    tokens = []
    try:
        for tok in tokenize.generate_tokens(StringIO(source).readline):
            token = Token(tok)
            if not token.string.strip():  # ignore spaces
                continue
            if token.type == tokenize.COMMENT:
                break
            tokens.append(token)
    except tokenize.TokenError as exc:
        print("#" * 50)
        print("WARNING: the following tokenize error was raised\n", exc)
        print("#" * 50)
        return tokens
    except Exception as exc:
        print("#" * 50)
        print("WARNING: the following exception was raised\n", exc)
        print("#" * 50)
        return tokens

    return tokens


def tokenize_source_lines(source_lines):
    """Makes a list of tokens from a source (list of lines),
       ignoring spaces and comments.
    """
    source = "\n".join(source_lines)
    return tokenize_source(source)


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


def print_token_table(source):
    """Prints tokens found in source, excluding spaces and comments.

       This is occasionally useful to use at the console during development.
    """
    print(
        _token_format.format(
            type="Type", string="String", start="Start", end="End", line="last"
        )
    )
    print("-" * 73)
    tokens = tokenize_source(source)
    for token in tokens:
        print(token)
