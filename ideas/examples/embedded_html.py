"""
embedded_html
-------------

This transform allows you to embed HTML in Python in a manner reminiscent of JSX
in JavaScript.

Embedded HTML is surrounded with the new operators `:(` and `):`.  Embedded HTML
is converted to a series of calls to `el(...)` which you must make sure is defined
in the context where your HTML appears.  An example is:

```
def el(name: str, attrs: dict[str, Union[str, bool]], *children):
    pass

def html(title:str, link_text:str, link_url:str):
    my_html = :(
        <div class="grid-3">
            <h1>{title}</h1>
            <p><a href="#top">Back to top</a></p>
            <p><a href={link_url}>{link_text}</a></p>
            <p>Some text - with an embedded value {title} - goes here</p>
        </div>
    ):

    return my_html
```

Whitespace within HTML text nodes is not exactly preserved but should be good
enough to preserve the same rendering.
"""
import logging
import tokenize
from typing import Optional, Union, Iterator, Iterable

from ideas import import_hook
import token_utils

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

PARENS = {"(": ")", "{": "}", "[": "]"}

Token = tuple[token_utils.Token, str]


def index_of(
    tokens: list[Token], token: str, start: int = 0, limit: Optional[int] = None
) -> Optional[int]:
    """
    Find the index of the first occurence of a token, starting at `start` in the list
    and looking no further than `limit`.  If `limit is None` then the whole list from
    `start` onwards is considered.

    Returns the index or `None` if no match.
    """
    for ii, tok in enumerate(tokens[start:limit]):
        if tok.string == token:
            return start + ii
    return None


def index_of_seq(
    tokens: list[Token], pattern: list[Token], start=0, limit: Optional[int] = None
) -> Optional[int]:
    """
    Find the index of the first occurence of a sequence of tokens, starting at
    `start` in the list and looking no further than `limit`.  If `limit is None`
    then the whole list beginning at `start` is considered.

    Returns the index, or `None` if no match.
    """
    pat_len = len(pattern)
    for ii in range(start, len(tokens) - pat_len + 1):
        if tokens[ii : ii + pat_len] == pattern:
            return ii
    return None


def print_tokens(line: list[str]) -> str:
    "Return a string representation of a list of tokens."
    return " ".join(f"[{x}]" for x in line)


def non_space_tokens(tokens: list[token_utils.Token]) -> Iterator[token_utils.Token]:
    "Yield non-space tokens in `tokens`."
    return filter(lambda x: not x.is_space(), tokens)


def stringify(tokens: list[Union[token_utils.Token, str]]) -> Optional[str]:
    """
    Convert `tokens` to a Python string, eg. for turning text elements in HTML into strings.

    Returns `None` if it would otherwise return an empty string.
    """
    log.debug("Stringifying %s", tokens)
    if tokens:
        str_val = "".join(f"{str(x)}" for x in tokens)
        if str_val.strip():
            return '"{}"'.format(str_val)
    return None


def extract_attrs(tokens: list[Token]) -> dict[str, Union[str, bool]]:
    """
    Read a list of HTML attributes and return them as a `dict`.
    """
    ii = 0
    while ii < len(tokens):
        name = tokens[ii]
        if ii + 1 == len(tokens):
            ii += 1
            yield name.string, True
            continue
        if tokens[ii + 1] == "=":
            if ii + 2 == len(tokens):
                raise SyntaxError(
                    f"Mal-formed HTML: {' '.join(str(t) for t in tokens)}"
                )
            elif tokens[ii + 2].string == "{":
                end_index = find_matching_paren(tokens, ii + 2)
                yield name.string, "".join(
                    token.string for token in tokens[ii + 3 : end_index]
                )
                ii = end_index + 1
            else:
                value = tokens[ii + 2]
                ii += 3
                yield name.string, value.string
            continue
        ii += 1
        yield name.string, True


def extract_string(
    tokens: Iterable[Token],
    prev_token: Token,
    next_token: Token,
    indent: str,
    lstrip: bool = False,
) -> str:
    """
    Extract a string, formatted exactly as it was in the source.

    Just pasting the token stream together is not good enough; the tokenizer
    ignores whitespace and so, for instance, the input `1+2` is indistinguishable
    from `1 + 2`.  But for HTML text such whichspace may be significant.

    So we extract the text from the source line.  Note that tokens on a single
    "line" as the HTML transform understands it may be from several pysical lines
    in the source file, because the HTML transform pastes all continuation lines
    together.  So the string that is constructed broadly follows HTML rules; it
    iterates over the tokens, looking for line breaks in the original source.
    When it finds a line break, it takes all the text up to there, removes the
    line break, adds a space and then removes the indent if it is present.  It
    then carries on with the next source line.
    """

    start_line, start_col = prev_token.end
    start_tok = tokens[0]
    text = ""

    for ii, token in enumerate(tokens):
        current_line, current_col = token.start
        if current_line != start_line:
            text += start_tok.line[start_col:]
            start_line, start_col = token.start
            start_tok = token
            if token.string.startswith(indent):
                start_col += len(indent)

    end_line, end_col = next_token.start
    if start_line != end_line:
        text += start_tok.line[start_col:]
    else:
        text += start_tok.line[start_col : end_col]
    log.warning("Text: %s", text)
    text = text.replace("\n", " ")
    if lstrip:
        text = text.lstrip()
    if text != text.rstrip():
        text = text.rstrip() + " "
    if not text:
        return None
    return f'"{text}"'


def extract_text(
    tokens: list[Token], start: int
) -> tuple[int, list[token_utils.Token]]:
    """
    Read an HTML text node, possibly including Python expressions surrounded with
    braces (`{}`).

    Reads from `tokens`, starting at index `ii`.

    Note that it is never valid for such a string to end a piece of HTML so we don't need
    to worry about the HTML end delimiter.

    Returns the next token to be processed and the list of tokens making up the text.
    """
    new_tokens = []
    end_index = index_of(tokens, "<", start) or len(tokens)
    log.debug("Considering tokens %s", tokens[start:end_index])
    ii = start
    while ii < end_index:
        expr_start = index_of(tokens, "{", ii, end_index)
        if expr_start is not None:
            expr_end = find_matching_paren(tokens, expr_start)
            if ii > start:
                new_tokens.append(" + ")
            if expr_start > ii:
                new_tokens += [
                    extract_string(
                        tokens[ii:expr_start],
                        tokens[ii - 1],
                        tokens[expr_start],
                        "",
                        ii == start,
                    ),
                    " + ",
                ]
            new_tokens += ["str( "] + tokens[expr_start + 1 : expr_end] + [")"]
            ii = expr_end + 1
        else:
            if ii > start:
                new_tokens.append(" + ")
            new_tokens.append(
                extract_string(
                    tokens[ii:end_index],
                    tokens[ii - 1],
                    tokens[end_index],
                    "",
                    ii == start,
                )
            )
            ii = end_index

    log.debug("Found string with content: %s", new_tokens)
    return ii, list(filter(lambda x: x is not None, new_tokens))


def attr_str(attrs: dict) -> str:
    """
    Render an attribute dictionary as a literal to be included in Python output.

    Note that this is different to a standard dict rendering because the quoting
    of the value is different.
    """
    return "{{{}}}".format(
        ", ".join(f'"{key}": {value}' for key, value in attrs.items())
    )


def extract_tag(
    tokens: list[Token], ii: int, tag_stack: list[Token]
) -> tuple[int, list[token_utils.Token]]:
    """
    Read an HTML element (start, end or self-closing) where one is expected.

    Reads from `tokens`, starting at index `ii`.
    """
    start_index = index_of(tokens, "<", ii)
    if start_index is None:
        return ii, []

    end_index = index_of(tokens, ">", start_index)
    if not end_index:
        raise SyntaxError("Ill-formed HTML tag")
    end_index += 1

    tag_tokens = tokens[start_index + 1 : end_index - 1]
    if not tag_tokens:
        raise SyntaxError("Ill-formed HTML tag")
    tag_content = list(tag_tokens)

    if tag_content[0].string == "/":
        if len(tag_content) != 2:
            raise SyntaxError("Ill-formed HTML tag")
        name = tag_tokens[1]
        if tag_stack[-1] != name:
            raise SyntaxError(f"Tag </{name}> cannot close <{tag_stack[-1]}>")
        tag_stack.pop()
        return end_index, ["    ),"]
    else:
        name = tag_content[0]
        attr_end = None
        closed = False
        if tag_content[-1] == "/":
            attr_end = -1
            closed = True
        else:
            tag_stack.append(name)
        attrs = {x: y for x, y in extract_attrs(tag_content[1:attr_end])}
        new = ["el", "(", f'"{name}"', ",", attr_str(attrs), ","]
        if closed:
            new.append("),")

        log.debug("Found tag with content: %s", new)
        return end_index, new


def space(tokens: Iterable[Token]) -> Iterator[Token]:
    """
    Yield a sequence of tokens with spaces inserted as appropriate to make it a
    bit more readable.
    """
    tokens = list(tokens)
    list_len = len(tokens)
    for ii, token in enumerate(tokens):
        if isinstance(token, token_utils.Token):
            yield token.string
            if (
                not token.is_space()
                and token.type != tokenize.INDENT
                and ii != list_len - 1
            ):
                yield " "
            continue
        yield token


def no_dedents(tokens: Iterable[Token]) -> Iterator[Token]:
    """
    Filter dedents out of a sequence of tokens.
    """
    for token in tokens:
        if isinstance(token, token_utils.Token):
            if token.type == tokenize.DEDENT:
                continue
        yield token


def simple_tokens(tokens: list[Token], with_newline: bool = True) -> str:
    """
    Return a simple string version of a list of tokens
    """
    return "".join(space(no_dedents(tokens))) + ("\n" if with_newline else "")


def remove_newlines(tokens: Iterable[Token]) -> Iterator[Token]:
    """Remove newlines from a stream of tokens."""
    for token in tokens:
        if isinstance(token, token_utils.Token):
            if token.type == tokenize.NEWLINE:
                continue
        else:
            if token == "\n":
                continue
        yield token


def remove_indents(tokens: Iterable[Token]) -> Iterator[Token]:
    for token in tokens:
        if isinstance(token, token_utils.Token):
            if token.type == tokenize.INDENT:
                continue
        yield token


def find_matching_paren(tokens: Iterable[Token], start: int) -> int:
    """
    Return the index of the closing parenthesis matching the opening one at index
    `start`.  `start` must point to an opening parenthesis.
    """
    parens = []
    for ii, token in enumerate(tokens[start:]):
        if token.string in PARENS:
            parens.append(token)
        if parens and token.string == PARENS[str(parens[-1])]:
            parens.pop()
        if not parens:
            return start + ii
    raise SyntaxError("Opening paren at %s has no matching close.", token.start)


def group_split_statements(lines: Iterable[list[Token]]) -> Iterator[Iterable[Token]]:
    """
    Convert a list of source code lines so that all statements are contained in a single line.
    """
    parens = []
    in_process = []
    indents = [""]

    for line in lines:
        for token in line:
            if token.type == tokenize.INDENT:
                indents.append(token.string)
            if token.type == tokenize.DEDENT:
                indents.pop()
            if token.string in PARENS:
                parens.append(token)
            if parens and token.string == PARENS[str(parens[-1])]:
                parens.pop()
        in_process += line
        if not parens:
            content = list(remove_newlines(remove_indents(in_process)))
            if not all(c.string.isspace() for c in content):
                yield [indents[-1]] + content
            else:
                yield ["\n"]
            in_process = []
        else:
            # There are unclosed groups, keep looking for closing tokens
            pass
    if in_process:
        # We finished the stream with unclosed groups.  Return what we have and
        # let the Python interpreter report the error.
        yield [indents[-1]] + list(remove_newlines(remove_indents(in_process)))


def extract_html(tokens: Iterable[Token], indent: str = "") -> Iterator[Token]:
    tag_stack = []
    new_tokens = []
    ii = token_utils.get_first_index(tokens)
    while ii < len(tokens):
        if tag_stack:
            ii, string = extract_text(tokens, ii)
            if string:
                new_tokens.append(indent + "    " * (len(tag_stack) + 1))
                new_tokens += string
                new_tokens.append(",")
                new_tokens.append("\n")
                continue
        else:
            start_idx = index_of(tokens, "<", ii)
            if start_idx is not None and start_idx != ii:
                new_tokens += simple_tokens(tokens[ii:start_idx])

        ii, tag_tokens = extract_tag(tokens, ii, tag_stack)
        if tag_tokens:
            new_tokens.append(indent + "    " * len(tag_stack))
            new_tokens += simple_tokens(tag_tokens)
            continue

        if ii == 0:
            new_tokens += simple_tokens(tokens[ii:], False)
        else:
            new_tokens += list(filter(lambda x: x != "\n", simple_tokens(tokens[ii:], False)))
        break

    return new_tokens


def transform_source(source: str, **_kwargs) -> str:
    """
    Transform HTML elements in source code into valid Python.

    HTML elements are surrounded by grouping operators `:(` and `):`.  The resemblance
    to sad and happy faces may not be entirely co-incidental.

    Each such group must contain exactly one top-level HTML tag.
    """

    from pprint import pformat

    log.debug(
        "Initial lines:\n%s",
        pformat(list(group_split_statements(token_utils.get_lines(source)))),
    )
    it = token_utils.get_lines(source)

    new_tokens = []

    for line in group_split_statements(it):
        ii = 0
        while ii < len(line):
            html_start = index_of_seq(line, [":", "("], ii)
            if html_start is None:
                log.warning("Simple line %s", line[ii:])
                pre_tokens = list(filter(lambda x: x != '\n', line[ii:]))
                pre_tokens = simple_tokens(pre_tokens)
                new_tokens += pre_tokens
                break

            html_end = index_of_seq(line, [")", ":"], html_start)
            if html_end is None:
                raise SyntaxError("HTML start :( does not have matching end ):")

            html_tokens = extract_html(
                line[html_start + 2 : html_end], line[0] if line[0].isspace() else ""
            )

            new_tokens += simple_tokens(line[:html_start], False)
            new_tokens.append(" (\n")
            new_tokens += simple_tokens(html_tokens, False)
            new_tokens += [")", "\n"]
            ii = html_end + 2

    new_source = token_utils.untokenize(new_tokens)
    log.debug("Transformed source:\n%s", new_source)
    return new_source


def add_hook(**_kwargs):
    hook = import_hook.create_hook(
        transform_source=transform_source, hook_name=__name__
    )
    return hook
