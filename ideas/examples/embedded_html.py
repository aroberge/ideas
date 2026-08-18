"""
embedded_html
-------------

This transform allows you to embed HTML in Python in a manner reminiscent of JSX
in JavaScript.

Embedded HTML is surrounded with the new operators `>>|` and `|<<`.  Embedded HTML
is converted to a series of calls to `el(...)` which you must make sure is defined
in the context where your HTML appears.  An example is:

```
def el(name: str, attrs: dict[str, Union[str, bool]], *children):
    pass

def html(title:str, link_text:str, link_url:str):
    my_html = >>|
        <div class="grid-3">
            <h1>{title}</h1>
            <p><a href="#top">Back to top</a></p>
            <p><a href={link_url}>{link_text}</a></p>
            <p>Some text - with an embedded value {title} - goes here</p>
        </div>
    |<<

    return my_html
```

Whitespace within HTML text nodes is not exactly preserved but should be good
enough to preserve the same rendering.

The delimiters can be changed by changing the `HTML_START` and `HTML_END`
constants below.
"""
import logging
import tokenize
from typing import Optional, Union, Iterator, Iterable

import token_utils

from ideas import import_hook

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

PARENS = {"(": ")", "{": "}", "[": "]"}
HTML_START = [">>", "|"]
HTML_END = ["|", "<<"]

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
    for idx, tok in enumerate(tokens[start:limit]):
        if tok.string == token:
            return start + idx
    return None


def index_of_seq(tokens: list[Token], pattern: list[Token], start=0) -> Optional[int]:
    """
    Find the index of the first occurence of a sequence of tokens, starting at
    `start` in the list and looking no further than `limit`.  If `limit is None`
    then the whole list beginning at `start` is considered.

    Returns the index, or `None` if no match.
    """
    pat_len = len(pattern)
    for idx in range(start, len(tokens) - pat_len + 1):
        if tokens[idx : idx + pat_len] == pattern:
            return idx
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
    if tokens:
        str_val = "".join(f"{str(x)}" for x in tokens)
        if str_val.strip():
            return f'"{str_val}"'
    return None


def extract_attrs(tokens: list[Token]) -> dict[str, Union[str, bool]]:
    """
    Read a list of HTML attributes and return them as a `dict`.
    """
    idx = 0
    while idx < len(tokens):
        name = tokens[idx]
        if idx + 1 == len(tokens):
            idx += 1
            yield name.string, True
            continue
        if tokens[idx + 1] == "=":
            if idx + 2 == len(tokens):
                raise SyntaxError(
                    f"Mal-formed HTML: {' '.join(str(t) for t in tokens)}"
                )
            if tokens[idx + 2].string == "{":
                end_index = find_matching_paren(tokens, idx + 2)
                yield name.string, "".join(
                    token.string for token in tokens[idx + 3 : end_index]
                )
                idx = end_index + 1
            else:
                value = tokens[idx + 2]
                idx += 3
                yield name.string, value.string
            continue
        idx += 1
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
    start_tok = prev_token
    text = ""

    for token in tokens:
        current_line, _ = token.start
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
        text += start_tok.line[start_col:end_col]
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

    Reads from `tokens`, starting at index `idx`.

    Note that it is never valid for such a string to end a piece of HTML so we don't need
    to worry about the HTML end delimiter.

    Returns the next token to be processed and the list of tokens making up the text.
    """
    new_tokens = []
    end_index = index_of(tokens, "<", start) or len(tokens)
    idx = start
    while idx < end_index:
        expr_start = index_of(tokens, "{", idx, end_index)
        if expr_start is not None:
            expr_end = find_matching_paren(tokens, expr_start)
            if idx > start:
                new_tokens.append(" + ")
            if expr_start > idx:
                new_tokens += [
                    extract_string(
                        tokens[idx:expr_start],
                        tokens[idx - 1],
                        tokens[expr_start],
                        "",
                        idx == start,
                    ),
                    " + ",
                ]
            new_tokens += ["str( "] + tokens[expr_start + 1 : expr_end] + [")"]
            idx = expr_end + 1
        else:
            if idx > start:
                new_tokens.append(" + ")
            new_tokens.append(
                extract_string(
                    tokens[idx:end_index],
                    tokens[idx - 1],
                    tokens[end_index],
                    "",
                    idx == start,
                )
            )
            idx = end_index

    return idx, list(filter(lambda x: x is not None, new_tokens))


def attr_str(attrs: dict) -> str:
    """
    Render an attribute dictionary as a literal to be included in Python output.

    Note that this is different to a standard dict rendering because the quoting
    of the value is different.
    """
    return "{{{}}}".format(  # pylint: disable=consider-using-f-string
        ", ".join(f'"{key}": {value}' for key, value in attrs.items())
    )


def extract_tag(tokens: list[Token], idx: int) -> tuple[int, tuple[int, str, dict]]:
    """
    Read an HTML element (start, end or self-closing) where one is expected.

    Reads from `tokens`, starting at index `idx`.
    """
    start_index = index_of(tokens, "<", idx)
    if start_index is None:
        return idx, (0, None, None)

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
        return end_index, (2, name.string, None)

    name = tag_content[0]
    attr_end = None
    closed = False
    if tag_content[-1] == "/":
        attr_end = -1
        closed = True
    attrs = dict(extract_attrs(tag_content[1:attr_end]))
    return end_index, (1 if not closed else 3, name.string, attrs)


def space(tokens: Iterable[Token]) -> Iterator[Token]:
    """
    Yield a sequence of tokens with spaces inserted as appropriate to make it a
    bit more readable.
    """
    tokens = list(tokens)
    list_len = len(tokens)
    for idx, token in enumerate(tokens):
        if isinstance(token, token_utils.Token):
            yield token.string
            if (
                not token.is_space()
                and token.type != tokenize.INDENT
                and idx != list_len - 1
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
    """
    Yield tokens, skipping any that are indents.
    """
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
    for idx, token in enumerate(tokens[start:]):
        if token.string in PARENS:
            parens.append(token)
        if parens and token.string == PARENS[str(parens[-1])]:
            parens.pop()
        if not parens:
            return start + idx
    assert tokens
    raise SyntaxError(f"Opening paren at {tokens[0].start} has no matching close.")


def group_split_statements(lines: Iterable[list[Token]]) -> Iterator[Iterable[Token]]:
    """
    Convert a list of source code lines so that all statements are contained in a single line.
    """
    parens = []
    in_process = []
    indents = [""]

    def handle_indents(token):
        if token.type == tokenize.INDENT:
            indents.append(token.string)
        elif token.type == tokenize.DEDENT:
            indents.pop()

    def handle_parens(idx, token, line):
        if token.string in PARENS:
            parens.append(token)
        elif parens and token.string == PARENS.get(str(parens[-1])):
            parens.pop()
        elif (
            idx < len(line) - len(HTML_START)
            and line[idx : idx + len(HTML_START)] == HTML_START
        ):
            parens.append(HTML_START)
        elif (
            idx < len(line) - len(HTML_END)
            and line[idx : idx + len(HTML_END)] == HTML_END
            and parens[-1] == HTML_START
        ):
            parens.pop()

    for line in lines:
        for idx, token in enumerate(line):
            handle_indents(token)
            handle_parens(idx, token, line)
        in_process += line
        if not parens:
            content = list(remove_newlines(remove_indents(in_process)))
            if not all(c.string.isspace() for c in content):
                yield indents[-1], content + ["\n"]
            else:
                yield "", ["\n"]
            in_process = []
        else:
            # There are unclosed groups, keep looking for closing tokens
            pass
    if in_process:
        # We finished the stream with unclosed groups.  Return what we have and
        # let the Python interpreter report the error.
        yield indents[-1], list(remove_newlines(remove_indents(in_process)))


HTML = Union[str, tuple[int, tuple[str, dict], list["html"]]]


def extract_html(tokens: Iterable[Token], indent: str = "") -> HTML:
    """
    Convert a list of tokens into HTML.  The tokens should not include the HTML
    delimiters.
    """
    idx = token_utils.get_first_index(tokens)
    # Opening tag
    idx, (typ, name, attrs) = extract_tag(tokens, idx)

    if typ == 3:
        # Self-closing tag
        return idx, (name, attrs), []

    if typ != 1:
        raise SyntaxError(f"Unexpected opening tag: <{name}>")

    # Children
    children = []
    while idx < len(tokens):
        next_tag_idx = index_of(tokens, "<", idx)

        if idx != next_tag_idx:
            idx, string = extract_text(tokens, idx)
            if string:
                children.append(string)
            continue

        next_idx, (next_typ, next_name, _) = extract_tag(tokens, idx)
        if next_typ == 2:
            if next_name != name:
                raise SyntaxError(
                    f"Closing tag </{next_name}> can't close tag <{name}>"
                )
            # Closing tag
            return next_idx, (name, attrs), children

        if next_typ == 0:
            continue

        next_idx, tag, next_children = extract_html(tokens[idx:], indent)
        children.append((idx, tag, next_children))
        idx += next_idx

    raise SyntaxError(f"Tag <{name}> is not closed")


def write_html(html: HTML) -> str:
    """
    Write embedded HTML as a series of function calls.
    """
    if isinstance(html, str):
        return html
    if isinstance(html, token_utils.Token):
        return html.string
    if isinstance(html, list):
        return "".join(str(x) for x in html)

    _, (tag, attrs), children = html
    return (
        f'el("{tag}", {attr_str(attrs)}, '
        + ", ".join(write_html(child) for child in children)
        + ")"
    )


def transform_source(source: str, **_kwargs) -> str:
    """
    Transform HTML elements in source code into valid Python.

    HTML elements are surrounded by grouping operators `>>|` and `|<<`.  The resemblance
    to sad and happy faces may not be entirely co-incidental.

    Each such group must contain exactly one top-level HTML tag.
    """

    lines_iter = token_utils.get_lines(source)

    new_tokens = []

    for indent, line in group_split_statements(lines_iter):
        line_contains_html = index_of_seq(line, HTML_START, 0) is not None
        idx = 0
        while idx < len(line):
            html_start = index_of_seq(line, HTML_START, idx)
            if html_start is None:
                if not line_contains_html:
                    new_tokens += line
                else:
                    pre_tokens = list(filter(lambda x: x != "\n", line[idx:]))
                    pre_tokens = simple_tokens(pre_tokens)
                    new_tokens += pre_tokens
                break

            html_end = index_of_seq(line, HTML_END, html_start)
            if html_end is None:
                raise SyntaxError(
                    f"HTML start {HTML_START} does not have matching end {HTML_END}"
                )

            html = extract_html(line[html_start + len(HTML_START) : html_end], "")

            html_tokens = write_html(html)

            new_tokens.append(indent)
            new_tokens += simple_tokens(line[:html_start], False)
            new_tokens.append(" (\n")
            new_tokens += simple_tokens(html_tokens, False)
            new_tokens += [")", "\n"]
            idx = html_end + len(HTML_END)

    new_source = token_utils.untokenize(new_tokens)
    return new_source


def add_hook(**_kwargs):
    """
    Install the embedded_html transform.
    """
    hook = import_hook.create_hook(
        transform_source=transform_source, hook_name=__name__
    )
    return hook
