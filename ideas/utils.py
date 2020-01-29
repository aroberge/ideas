"""utils.py

A few useful objects which do not naturally fit anywhere else.
"""
import keyword
import token as token_module
import tokenize
import os.path
import sys

from io import StringIO

_token_format = "type={type}  string={string}  start={start}  end={end}  line='{line}'"


class Token:
    """Token as generated from tokenize.generate_tokens written here in
       a more convenient form for our purpose. The various
       paramters are::

           type: token type
           string: the token written as a string
           start = (start_line, start_col)
           end = (end_line, end_col)
           line: entire line of code where the token is found.
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
            type="%s (%s)" % (self.type, token_module.tok_name[self.type]),
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

    except tokenize.TokenError as exc:
        print("#" * 50)
        print("WARNING: the following tokenize error was raised\n", exc)
        print("#" * 50)
    except Exception as exc:
        print("#" * 50)
        print("WARNING: the following exception was raised\n", exc)
        print("#" * 50)

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
            if token.start_line != current_line:
                current_line = token.start_line
                if new_line:
                    lines.append(new_line)
                new_line = []
            new_line.append(token)
    except tokenize.TokenError as exc:
        print("#" * 50)
        print("WARNING: the following tokenize error was raised\n", exc)
        print("#" * 50)
    except Exception as exc:
        print("#" * 50)
        print("WARNING: the following exception was raised\n", exc)
        print("#" * 50)

    if new_line:
        lines.append(new_line)
    return lines


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
    tokens = tokenize_source(source)
    for token in tokens:
        print(token)


def change_path_for_testing(name, remove=False):
    """This function is useful for testing.
    """
    this_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    example_dir = os.path.abspath(os.path.join(this_dir, "examples", name))
    if remove:
        if example_dir in sys.path:
            sys.path.remove(example_dir)
    elif os.path.exists(example_dir) and example_dir not in sys.path:
        sys.path.insert(0, example_dir)
