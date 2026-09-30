"""
Friendlier floats
=====================

Documentation to be written.

Add https://github.com/aroberge/experimental/blob/master/experimental/transformers/approx.py

Include math.isclose and cmath.isclose

≈
~

"""

import builtins
import sys
from fractions import Fraction
from ideas import create_hook
import token_utils


def __str__(self):
    if self._denominator == 1:  # noqa
        return str(self._numerator)  # noqa
    else:
        return str(float(self._numerator / self._denominator))  # noqa


Fraction.__str__ = __str__
Fraction.__repr__ = __str__


def display_hook(value):
    builtins._ = value
    if isinstance(value, complex):
        print(f" ≈ {str(value)}\n")
    elif isinstance(value, float):
        str_ = str(value)
        if str_.endswith(".0"):
            str_ = str_[:-2]
        print(f"~{str_}\n")
    elif isinstance(value, Fraction):
        print(value, "\n")
    else:
        print(value)


def transform_source(source, **_kwargs):
    """Replace integers (followed by /) as well as float numbers
    by Fraction objects. For floating point numbers, the denominator
    is limited to be 1e15, which makes it possible to create simple and
    intuitive representations of floats with 'a few' decimal places.
    For example, 0.1 will be represented as 1/10 - as expected.

    We also use Pyrets' notation to precede a float by ~ to keep it unchanged.
    """
    tokens = token_utils.tokenize(source)

    new_tokens = []
    tilde_was_found = False
    syntax_error = False

    for token, next_, after_ in token_utils.sliding_window(tokens, 3):
        if tilde_was_found:
            if token.is_integer():
                token.string = token.string + ".0"  # turn into a float
                tilde_was_found = False
            elif token.is_float() or token.is_complex():
                tilde_was_found = False
            new_tokens.append(token)
            continue

        if token == "~":
            if not token.is_immediately_before(next_):
                syntax_error = True
            elif not (next_.is_in(["+", "-"]) or next_.is_number()):
                syntax_error = True
            elif next_.is_in(["+", "-"]) and not next_.is_immediately_before(after_):
                syntax_error = True
            elif next_.is_in(["+", "-"]) and not after_.is_number():
                syntax_error = True
            else:
                tilde_was_found = True
                token.string = ""

            if syntax_error:
                print("Syntax error: ~ must immediately preceed a number\n")
                return ""
            new_tokens.append(token)
            continue

        # from here on, tilde did not preceed a number
        if token.is_float():
            token.string = (
                f"Fraction('{token.string}').limit_denominator(1_000_000_000_000_000)"
            )
        elif token.is_integer():
            token.string = f"Fraction({token.string})"

        new_tokens.append(token)
    return token_utils.untokenize(new_tokens)


def source_init():
    """Adds required import so that ``Fraction`` is a known object."""
    import_fraction = "from fractions import Fraction\n"
    return import_fraction


def add_hook(**_kwargs):
    """Creates and automatically adds the import hook in sys.meta_path."""
    sys.displayhook = display_hook

    hook = create_hook(
        name=__name__,
        console_only=True,
        source_init=source_init,
        transform_source=transform_source,
    )
    return hook
