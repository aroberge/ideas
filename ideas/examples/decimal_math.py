"""
This replaces any explicit float by a Decimal.
It can be used either as a custom codec or import hook.
"""

from ideas import custom_encoding, create_hook
import token_utils


def source_init():
    """Adds required import"""
    return "from decimal import Decimal\n"


def transform_source(source, **_kwargs):
    """Simple transformation: replaces any explicit float by a Decimal.

    By defining this function, we can also make use of Ideas' console.
    """
    tokens = token_utils.tokenize(source)
    for token in tokens:
        if token.is_number() and "." in token.string:
            token.string = f"Decimal('{token.string}')"

    return token_utils.untokenize(tokens)


def register():
    custom_encoding.register_encoding(
        encoding_name="decimal_math",
        transform_source=transform_source,
        name=__name__,
    )


def add_hook():
    """Creates and automatically adds the import hook in sys.meta_path"""
    hook = create_hook(
        name=__name__,
        source_init=source_init,
        transform_source=transform_source,
    )
    return hook
