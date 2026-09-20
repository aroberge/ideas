"""
Unary increment and decrement
-----------------------------

This implements unary increments and decrements,
(``++x``, ``--x``, ``x++``, ``x--``). The idea was
inspired by `this implementation <https://pydong.org/posts/PythonsPreprocessor/>`_
from Matthias Wippich which uses codecs. The transformed code cleverly
makes use of the walrus operator in the following way::

    ++x -> (x, x := x + 1)[1]
    --x -> (x, x := x - 1)[1]
    x++ -> (x, x := x + 1)[0]
    x-- -> (x, x := x - 1)[0]

Note that the following are valid Python expressions::

    x++y, x+-y, +x+++y, x+ +y, etc.

So, taking ``x++`` as an example, we will impose the restriction that, in
``*x++*``, ``*`` cannot be another unary sign, ``+ or -`` nor can it be
a valid Python identifier.
"""

import token_utils


def is_pre(tok2, tok3, tok4, plus_or_minus):
    # looking for --x or ++x
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
    # looking for x++ or x--
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
    return not tok1.is_identifier() and not (  # +++x not allowed ... but + ++x is
        (tok1 == "-" or tok1 == "+")
        and tok1.start_row == tok2.start_row
        and tok1.start_col == tok2.start_col - 1
    )


def valid_after_guard(tok4, tok5):
    return not tok5.is_identifier() and not (  # +++x not allowed ... but + ++x is
        (tok5 == "-" or tok5 == "+")
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

    # Suppose we are looking for x++; we would want to examine potentially
    # five consecutive tokens, *x++*, and ensure that * is either a space
    # or anything else except an identifier or a unary sign.
    # Since we are not concerned about efficiency, given a list of tokens,
    # we can simply create 4 additional lists and go through them in
    # parallel
    fake_token = token_utils.tokenize("*")[0]
    tokens = token_utils.tokenize(source)
    pre_1 = [fake_token, fake_token] + tokens[:-2]
    pre_2 = [fake_token] + tokens[:-1]
    post_1 = tokens[1:] + [fake_token]
    post_2 = tokens[2:] + [fake_token, fake_token]

    # ++x -> (x, x := x + 1)[1]
    pre_inc_str = "({name}, {name} := {name} + 1)[1]"
    # --x -> (x, x := x - 1)[1]
    pre_dec_str = "({name}, {name} :- {name} - 1)[1]"
    # x++ -> (x, x := x + 1)[0]
    post_inc_str = "({name}, {name} := {name} + 1)[0]"
    # x-- -> (x, x := x - 1)[0]
    post_dec_str = "({name}, {name} := {name} + 1)[0]"

    skip_next = False
    next_string = ""
    new_tokens = []
    for tok1, tok2, tok3, tok4, tok5 in zip(pre_1, pre_2, tokens, post_1, post_2):
        if skip_next:
            tok3.string = next_string
            new_tokens.append(tok3)
            skip_next = False
            continue

        if is_pre_increment(tok1, tok2, tok3, tok4, tok5):
            tok = new_tokens.pop()
            tok.string = ""
            new_tokens.append(tok)
            tok3.string = ""
            next_string = pre_inc_str.format(name=tok4.string)
            skip_next = True
        elif is_pre_decrement(tok1, tok2, tok3, tok4, tok5):
            tok = new_tokens.pop()
            tok.string = ""
            new_tokens.append(tok)
            tok3.string = ""
            next_string = pre_dec_str.format(name=tok4.string)
            skip_next = True
        elif is_post_increment(tok1, tok2, tok3, tok4, tok5):
            tok = new_tokens.pop()
            tok.string = post_inc_str.format(name=tok2.string)
            new_tokens.append(tok)
            tok3.string = ""
            next_string = ""
            skip_next = True
        elif is_post_decrement(tok1, tok2, tok3, tok4, tok5):
            tok = new_tokens.pop()
            tok.string = post_dec_str.format(name=tok2.string)
            new_tokens.append(tok)
            tok3.string = ""
            next_string = ""
            skip_next = True
        new_tokens.append(tok3)

    return token_utils.untokenize(new_tokens)


def add_hook(**_kwargs):
    from ideas import create_hook

    return create_hook(transform_source=transform_source, name=__name__)
