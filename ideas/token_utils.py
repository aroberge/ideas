"""token_utils.py

A collection of useful functions and methods to deal with tokenizing
source code.
"""
import keyword
import tokenize as py_tokenize

from io import StringIO

_token_format = "type={type}  string={string}  start={start}  end={end}  line={line}"


class Token:
    """Token as generated from Python's tokenize.generate_tokens written here in
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
        """Returns True if the token represents a valid Python identifier
        excluding Python keywords.

        Note: this is different from Python's string method ``isidentifier``
        which also returns True if the string is a keyword.
        """
        return self.string.isidentifier() and not self.is_keyword()

    def is_comment(self):
        """Returns True if the token is a comment."""
        return self.type == py_tokenize.COMMENT

    def is_space(self):
        """Returns True if the token indicates a change in indentation,
        the end of a line, or the end of the source.
        """
        return self.type in (
            py_tokenize.INDENT,
            py_tokenize.NEWLINE,
            py_tokenize.NL,
            py_tokenize.DEDENT,
            py_tokenize.ENDMARKER,
        )

    def is_newline(self):
        """Returns True if token is a type of new line (NEWLINE or NL)."""
        return self.type in (py_tokenize.NEWLINE, py_tokenize.NL)

    def __repr__(self):
        """Nicely formatted token to help with debugging session.

        Note that it does **not** print a string representation that could be
        used to create a new ``Token`` instance, which is something you should
        never need to do other than indirectly by using the functions
        provided in this module.
        """
        return _token_format.format(
            type="%s (%s)" % (self.type, py_tokenize.tok_name[self.type]),
            string=repr(self.string),
            start=str(self.start),
            end=str(self.end),
            line=repr(self.line),
        )


def tokenize(source):
    """Transforms a source (string) into a list of Tokens."""
    tokens = []

    try:
        for tok in py_tokenize.generate_tokens(StringIO(source).readline):
            token = Token(tok)
            tokens.append(token)
    except (py_tokenize.TokenError, Exception) as exc:
        print(
            "WARNING: the following error was raised in",
            f"{__name__}.tokenize\n",
            exc,
        )

    return tokens


def get_lines(source):
    """Transforms a source (string) into a list of Tokens, with each
    (inner) list containing all the tokens found on a given line of code.
    """
    lines = []
    current_row = -1
    new_line = []
    try:
        for tok in py_tokenize.generate_tokens(StringIO(source).readline):
            token = Token(tok)
            if token.start_row != current_row:
                current_row = token.start_row
                if new_line:
                    lines.append(new_line)
                new_line = []
            new_line.append(token)
    except (py_tokenize.TokenError, Exception) as exc:
        print("###\nWARNING: the following tokenize error was raised\n", exc, "\n###")

    if new_line:
        lines.append(new_line)
    return lines


def get_number(tokens, ignore_comments=False):
    """Given a list of tokens, gives a count of the number of
    tokens which are NOT space tokens (such as NEWLINE, INDENT, DEDENT, etc.)

    If ``ignore_comments`` is set to ``True``, COMMENT tokens are also excluded.
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
    (such as a NEWLINE, INDENT, DEDENT, etc.)

    Returns ``None`` if none is found.
    """
    for token in tokens:
        if not token.is_space():
            return token
    return None


def get_first_index(tokens):
    """Given a list of tokens, find the index of the first one which is
    not a space token (such as a NEWLINE, INDENT, DEDENT, etc.)

    Returns ``None`` if none is found.
    """
    for index, token in enumerate(tokens):
        if not token.is_space():
            return index
    return None


def get_last(tokens, exclude_comment=True):
    """Given a list of tokens, find the last token which is not a space token
    (such as a NEWLINE, INDENT, DEDENT, etc.).

    By default, COMMENT tokens are excluded.

    Returns ``None`` if none is found.
    """
    for token in reversed(tokens):
        if exclude_comment:
            if not token.is_space() and not token.is_comment():
                return token
        else:
            if not token.is_space():
                return token
    return None


def get_last_index(tokens, exclude_comment=True):
    """Given a list of tokens, find the index of the last token which is
    not a space token (such as a NEWLINE, INDENT, DEDENT, etc.).

    By default, COMMENT tokens are excluded.

    Returns ``None`` if none is found.
    """
    for index, token in enumerate(reversed(tokens)):
        if exclude_comment:
            if not token.is_space() and not token.is_comment():
                return len(tokens) - index
        else:
            if not token.is_space():
                return len(tokens) - index
    return None


def dedent(tokens, dedent):
    """Given a list of tokens, produces an equivalent list corresponding
    to a line of code with dedent characters removed.
    """
    line = untokenize(tokens)
    line = line[dedent:]
    return tokenize(line)

# untokenize adapted from https://github.com/myint/untokenize
# Copyright (C) 2013-2018 Steven Myint
# MIT License - same as this project
#


def untokenize(tokens):
    """Return source code based on tokens.

    This is similar to Python's own tokenize.untokenize(), except that it
    preserves spacing between tokens, by using the line
    information recorded by Python's tokenize.generate_tokens.
    As a result, if the original soure code had multiple spaces between
    some tokens or if escaped newlines were used or if tab characters
    were present in the original source, those will also be present
    in the source code produced by untokenize.

    Thus ``source == untokenize(tokenize(source))``.

    IMPORTANT: When modifying a list of tokens, do not remove a token
    from the original list of tokens prior to calling untokenize;
    instead, set its string attribute to an empty string.
    If you need to insert a token into an existing list,
    simply insert it as a string (and not as a Token instance).

    If a given item is a string instead of a Token object, it is simply
    added as is by ``untokenize``.

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
        if token.type == py_tokenize.ENCODING:
            continue

        # Preserve escaped newlines.
        if (
            last_non_whitespace_token_type != py_tokenize.COMMENT
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

       Source is either a string to be tokenized, or a list of Token objects.

       This is occasionally useful as a debugging tool.
    """
    if isinstance(source[0], Token):
        tokens = source
    else:
        tokens = tokenize(source)
    for token in tokens:
        print(token)
