"""token_utils.py

A collection of useful functions and methods to deal with tokenizing
source code.
"""
import keyword
import tokenize

from io import StringIO

_token_format = "type={type}  string={string}  start={start}  end={end}  line='{line}'"


class Token:
    """Token as generated from tokenize.generate_tokens written here in
    a more convenient form, and with some custom methods.

    The various parameters are::

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

    def __eq__(self, other):
        """Compares a Token with another object; returns true if
           self.string == other.string or if self.string == other.
        """
        if hasattr(other, "string"):
            return self.string == other.string
        elif isinstance(other, str):
            return self.string == other
        else:
            raise TypeError(
                "A token can only be compared to another token or to a string."
            )

    def is_keyword(self):
        """Returns True if the token represents a Python keyword.
        """
        return keyword.iskeyword(self.string)

    def is_identifier(self):
        """Returns True if the token is a Python identifier and not a Python keyword"""
        return self.string.isidentifier() and not self.is_keyword()

    def is_comment(self):
        """Returns True if the token is a comment"""
        return self.type == tokenize.COMMENT

    def is_space(self):
        """Returns True if the token indicates a change in indentation,
           the end of a line, or the end of the source.
        """
        return self.type in (
            tokenize.INDENT,
            tokenize.NEWLINE,
            tokenize.NL,
            tokenize.DEDENT,
            tokenize.ENDMARKER,
        )

    def is_newline(self):
        """Returns True if token is NEWLINE or NL"""
        return self.type in (tokenize.NEWLINE, tokenize.NL)

    def __repr__(self):
        """Nicely formatted token"""
        return _token_format.format(
            type="%s (%s)" % (self.type, tokenize.tok_name[self.type]),
            string=repr(self.string),
            start=str(self.start),
            end=str(self.end),
            line=repr(self.line),
        )


def tokenize_source(source):
    """Makes a list of tokens from a source (str)."""
    tokens = []

    try:
        for tok in tokenize.generate_tokens(StringIO(source).readline):
            token = Token(tok)
            tokens.append(token)
    except (tokenize.TokenError, Exception) as exc:
        print(
            "WARNING: the following error was raised in",
            f"{__name__}.tokenize_source\n",
            exc,
        )

    return tokens


def get_lines_of_tokens(source):
    """Makes a list of lists of tokens, with each (inner) list containing
       all the tokens found on a given line of code.
    """
    lines = []
    current_row = -1
    new_line = []
    try:
        for tok in tokenize.generate_tokens(StringIO(source).readline):
            token = Token(tok)
            if token.start_row != current_row:
                current_row = token.start_row
                if new_line:
                    lines.append(new_line)
                new_line = []
            new_line.append(token)
    except (tokenize.TokenError, Exception) as exc:
        print("###\nWARNING: the following tokenize error was raised\n", exc, "\n###")

    if new_line:
        lines.append(new_line)
    return lines


def get_number(tokens, ignore_comments=False):
    """Given a list of tokens, gives a count of the number of
    tokens which are NOT space tokens (such as newline, indent, dedent, etc.)

    If ignore_comments is set to True, comments are ignored as well.
    """
    nb = len(tokens)
    for token in tokens:
        if token.is_space():
            nb -= 1
        elif ignore_comments and token.is_comment():
            nb -= 1
    return nb


def get_first(tokens):
    """Given a list of tokens, find the first token which is not a space token
    (such as a newline, indent, dedent, etc.)

    Returns None if none is found.
    """
    for token in tokens:
        if not token.is_space():
            return token
    return None


def get_first_index(tokens):
    """Given a list of tokens, find the index of the first one which is
    not a space token (such as a newline, indent, dedent, etc.)

    Returns -1 if none is found.
    """
    for index, token in enumerate(tokens):
        if not token.is_space():
            return index
    return -1


def get_last(tokens, exclude_comment=True):
    """Given a list of tokens, find the last token which is not a space token
    (such as a newline, indent, dedent, etc.).

    By default, COMMENT tokens are excluded.

    Returns None if none is found.
    """
    for token in reversed(tokens):
        if exclude_comment:
            if not token.is_space() and not token.is_comment():
                return token
        else:
            if not token.is_space():
                return token
    return None


# untokenize adapted from https://github.com/myint/untokenize
#
# TODO: acknowledge it properly in documentation with license added
#


def untokenize(tokens):
    """Return source code based on tokens.

    This is similar to Python's tokenize.untokenize(), except that it
    preserves spacing between tokens, by using the line
    information recorded by Python's tokenize.generate_tokens.
    As a result, if the original soure code had multiple spaces between
    some tokens or if escaped newlines were used, those things will be
    reflected by untokenize.

    If a given item is a string instead of a Token object, it is simply
    added as is.

    IMPORTANT: do not remove a token from the original list of
    tokens prior to calling untokenize; instead, set its string attribute
    to an empty string.

    Note that if some tokens are changed, the line information will
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
    last_non_whitespace_token_type = None

    for token in tokens:
        if isinstance(token, str):
            words.append(token)
            continue
        if token.type == tokenize.ENCODING:
            continue

        # Preserve escaped newlines.
        if (
            last_non_whitespace_token_type != tokenize.COMMENT
            and token.start_row > last_row
        ):
            if previous_line.endswith(("\\\n", "\\\r\n", "\\\r")):
                words.append(previous_line[len(previous_line.rstrip(" \t\n\r\\")) :])

        # Preserve spacing.
        if token.start_row > last_row:
            last_column = 0
        if token.start_col > last_column:
            words.append(token.line[last_column : token.start_col])

        words.append(token.string)

        previous_line = token.line
        last_row = token.end_row
        last_column = token.end_col
        if not token.is_space():
            last_non_whitespace_token_type = token.type

    return "".join(words)


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
