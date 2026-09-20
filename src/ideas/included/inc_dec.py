"""
Unary increment and decrement operators
----------------------------------------

This implements unary pre/post increments and decrements operators,
(``++x``, ``--x``, ``x++``, ``x--``). These operators are well-liked
by some, but can be a huge source of confusion. In case you are not
familiar with them:

  - Pre-increment (``++x``) and pre-decrement (``--x``) operators modify their operand (``x``)
    by 1 and return the value **after** having done so. One question one might have is
    *what exactly is meant by 'after'?*.  For example, in some implementation of C,
    the expression ``y = x- --x`` is considered to be indefined: do we decrement ``x`` after
    doing the assignment or before? Also note that, in Python, we have
    that ``++x == x == --x`` is syntactically valid.

  - Post-increment (``x++``) and post-decrement (``x--``) operators also modify their
    operand by 1 but return the value before doing so. Note that, in Python, these
    expressions, ``x++`` and ``x--`` anre **not** syntactically valid.


The idea to implement these operators via an import hook was
inspired by `this implementation <https://pydong.org/posts/PythonsPreprocessor/>`_
from Matthias Wippich which uses codecs and token-based transformations.
Both Wippich's implementation, and that of
`Github user dankeyy <https://github.com/dankeyy/incdec.py/>`_
(using regular expression and codecs-based)
make cleverly use of the walrus operator in the following way::

    ++x -> (x, x := x + 1)[1]
    --x -> (x, x := x - 1)[1]
    x++ -> (x, x := x + 1)[0]
    x-- -> (x, x := x - 1)[0]

Note that the following are valid Python expressions::

    x++y, x+-y, +x+++y, x+ +y, etc.

While greatly inspired by the existing implementations, we have found that
they fail to give the expected result in some situations.
Our implementation takes care to ensure that these valid expressions
remain so with their current meaning; this is done by only making changes
when a human reader would be able to unambiguously identify if an
increment or decrement operator is used.

So, taking ``x++`` as an example, we will impose the restriction that, in
``*x++*``, ``*`` cannot be another unary sign, ``+ or -`` nor can it be
a valid Python identifier. In ``*x++*`` and similar, if ``*`` represent
an identifier, then spaces between
``*`` and the increment/decrement are not significant. Since we can't have
two consecutive identifiers in Python, no change will take place.
However, in ``x++``, there can be no space between any of these symbols.

Here's a sample session illustrating the transformations that do or do
not occur::

    > ideas -a inc_dec
    Ideas Console version 0.3.3. [Python version: 3.11.9]
    ideas> from ideas import transform
    ideas> transform("x++")
    (x, x := x + 1)[0]
    ideas> transform("x--")
    (x, x := x + 1)[0]
    ideas> transform("--x")
    (x, x := x - 1)[1]
    ideas> transform("++x")
    (x, x := x + 1)[1]

    ideas> transform("x+++")
    x+++
    ideas> transform("---x")
    ---x
    ideas> transform("x++y")
    x++y
    ideas> transform("x++ y") # think of 'x++' as a new value 'X', and thus 'X y'
    x++ y                     # which would be invalid; so we keep the valid syntax
    ideas> transform("x++ +y")
    (x, x := x + 1)[0] +y
    ideas> transform("'x++'")  # inside string
    'x++'
    ideas> transform("y-   ++x")
    y-   (x, x := x + 1)[1]
    ideas> transform("y-++x")  # valid Python syntax
    y-++x
"""

import token_utils


def is_pre(tok2, tok3, tok4, plus_or_minus):
    """Focuses on identifying if the three tokens represent
    a possible identifier immediately preceded by ++ or --"""
    return (
        tok2 == plus_or_minus
        and tok3 == plus_or_minus
        and tok3.start_row == tok2.start_row
        and tok3.start_col == tok2.start_col + 1  # no space between them
        and tok4.is_identifier()
        and tok4.start_row == tok3.start_row
        and tok4.start_col == tok3.start_col + 1
    )


def is_post(tok2, tok3, tok4, plus_or_minus):
    """Focuses on identifying if the three tokens represent
    a possible identifier immediately followed by ++ or --"""
    return (
        tok2.is_identifier()
        and tok3 == plus_or_minus
        and tok4 == plus_or_minus
        and tok3.start_row == tok2.start_row
        and tok3.start_col == tok2.start_col + 1  # no space between them
        and tok4.start_row == tok3.start_row
        and tok4.start_col == tok3.start_col + 1
    )


def valid_before_guard(tok1, tok2):
    return not tok1.is_identifier() and not (
        (tok1 == "-" or tok1 == "+")  # +++x not allowed ... but + ++x is
        and tok1.start_row == tok2.start_row
        and tok1.start_col == tok2.start_col - 1
    )


def valid_after_guard(tok4, tok5):
    return not tok5.is_identifier() and not (
        (tok5 == "-" or tok5 == "+")  # +++x not allowed ... but + ++x is
        and tok4.start_row == tok5.start_row
        and tok4.start_col == tok5.start_col - 1
    )


def is_pre_increment(tok1, tok2, tok3, tok4, tok5):
    return (
        is_pre(tok2, tok3, tok4, "+")
        and valid_before_guard(tok1, tok2)
        and valid_after_guard(tok4, tok5)
    )


def is_pre_decrement(tok1, tok2, tok3, tok4, tok5):
    return (
        is_pre(tok2, tok3, tok4, "-")
        and valid_before_guard(tok1, tok2)
        and valid_after_guard(tok4, tok5)
    )


def is_post_increment(tok1, tok2, tok3, tok4, tok5):
    return (
        is_post(tok2, tok3, tok4, "+")
        and valid_before_guard(tok1, tok2)
        and valid_after_guard(tok4, tok5)
    )


def is_post_decrement(tok1, tok2, tok3, tok4, tok5):
    return (
        is_post(tok2, tok3, tok4, "-")
        and valid_before_guard(tok1, tok2)
        and valid_after_guard(tok4, tok5)
    )


def transform_source(source, **_kwargs):
    """Transforms expressions such as ``x++`` into their appropriate
    Python equivalent."""

    # Suppose we are looking for x++; we would want to examine potentially
    # five consecutive tokens, *x++*, and ensure that * is either a space
    # or anything else except an identifier or a unary sign.
    # Since we are not concerned about efficiency, given a list of tokens,
    # we can simply create 4 additional lists and go through them in
    # parallel
    tokens = token_utils.tokenize(source)

    fake_token = token_utils.tokenize("*")[0]
    pre_1 = [fake_token, fake_token] + tokens[:-2]
    pre_2 = [fake_token] + tokens[:-1]
    post_1 = tokens[1:] + [fake_token]
    post_2 = tokens[2:] + [fake_token, fake_token]

    # ++x -> (x, x := x + 1)[1]
    pre_inc_str = "({name}, {name} := {name} + 1)[1]"
    # --x -> (x, x := x - 1)[1]
    pre_dec_str = "({name}, {name} := {name} - 1)[1]"
    # x++ -> (x, x := x + 1)[0]
    post_inc_str = "({name}, {name} := {name} + 1)[0]"
    # x-- -> (x, x := x - 1)[0]
    post_dec_str = "({name}, {name} := {name} - 1)[0]"

    skip_next = False
    next_string = ""
    new_tokens = []
    # Given the description above, tok1 and tok5 are the guards,
    # and the identifier is either tok2 (x++, x==) or tok4 (++x, --x)
    # The token from the original list is tok3: this is the one we focus
    # on looping on and appending
    for tok1, tok2, tok3, tok4, tok5 in zip(pre_1, pre_2, tokens, post_1, post_2):
        if skip_next:
            tok3.string = next_string  # tok4 from previous loop
            new_tokens.append(tok3)
            skip_next = False
            continue

        if is_pre_increment(tok1, tok2, tok3, tok4, tok5):
            tok = new_tokens.pop()  # tok2
            tok.string = ""
            new_tokens.append(tok)
            tok3.string = ""
            next_string = pre_inc_str.format(name=tok4.string)
            skip_next = True
        elif is_pre_decrement(tok1, tok2, tok3, tok4, tok5):
            tok = new_tokens.pop()  # tok2
            tok.string = ""
            new_tokens.append(tok)
            tok3.string = ""
            next_string = pre_dec_str.format(name=tok4.string)
            skip_next = True
        elif is_post_increment(tok1, tok2, tok3, tok4, tok5):
            tok = new_tokens.pop()
            tok.string = post_inc_str.format(name=tok2.string)
            new_tokens.append(tok)  # tok2
            tok3.string = ""
            next_string = ""
            skip_next = True
        elif is_post_decrement(tok1, tok2, tok3, tok4, tok5):
            tok = new_tokens.pop()
            tok.string = post_dec_str.format(name=tok2.string)
            new_tokens.append(tok)  # tok2
            tok3.string = ""
            next_string = ""
            skip_next = True
        new_tokens.append(tok3)

    return token_utils.untokenize(new_tokens)


def add_hook(**_kwargs):
    from ideas import create_hook

    return create_hook(transform_source=transform_source, name=__name__)
