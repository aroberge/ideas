"""
Rational math
==============

Documentation to be written.
"""
from ideas import import_hook
import token_utils


def transform_source(source, **_kwargs):
    """Replace integers (followed by /) as well as float numbers
    by Fraction objects. For floating point numbers, the denominator
    is limited to be 1e12, which makes it possible to create simple and
    intuitive representations of floats with 'a few' decimal places.
    For example, 0.1 will be represented as 1/10 - as expected.
    """
    tokens = token_utils.tokenize(source)

    new_tokens = []
    for token, next_ in zip(tokens, tokens[1:]):
        if token.is_float():
            token.string = (
                f"Fraction('{token.string}').limit_denominator(1_000_000_000_000)"
            )
        elif token.is_integer() and next_ == "/":
            token.string = f"Fraction({token.string})"
        new_tokens.append(token)
    last_token = tokens[-1]
    if last_token.is_float():
        last_token.string = (
            f"Fraction('{last_token.string}').limit_denominator(1_000_000_000_000)"
        )
    new_tokens.append(last_token)

    return token_utils.untokenize(new_tokens)


def source_init():
    """Adds required import so that ``Fraction`` is a known object."""
    import_fraction = "from fractions import Fraction\n"
    return import_fraction


def add_hook(**_kwargs):
    """Creates and automatically adds the import hook in sys.meta_path."""
    hook = import_hook.create_hook(
        hook_name=__name__,
        source_init=source_init,
        transform_source=transform_source,
    )
    return hook
