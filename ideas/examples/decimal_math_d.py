"""decimal_math_d.py
------------------------

This replaces any explicit float followed by ``D``, by a Decimal.
"""

from ideas import create_hook
import token_utils


def source_init():
    """Adds required import"""
    return "from decimal import Decimal\n"


def transform_source(source, **_kwargs):
    """Simple transformation: replaces any explicit float followed by ``D``
    by a Decimal.
    """
    tokens = token_utils.tokenize(source)
    for first, second in zip(tokens, tokens[1:]):
        if first.is_number() and "." in first.string and second == "D":
            first.string = f"Decimal('{first.string}')"
            second.string = ""

    return token_utils.untokenize(tokens)


def add_hook():
    """Creates and automatically adds the import hook in sys.meta_path"""
    hook = create_hook(
        name=__name__,
        source_init=source_init,
        transform_source=transform_source,
    )
    return hook
