"""
Converts integers literals that are followed by the ``/`` operator
into instances of the Fraction class in the source using the tokenizer.

It is only meant as an alternative to the AST transformation demo.
"""
from ideas import import_hook
import token_utils


def transform_source(source, **_kwargs):
    """Replace integers (followed by /) by Fraction objects"""
    tokens = token_utils.tokenize(source)
    if len(tokens) < 3:
        return source

    new_tokens = []
    for token, next_ in zip(tokens, tokens[1:]):
        if token.is_integer() and next_ == "/":
            token.string = f"Fraction({token.string})"
        new_tokens.append(token)
    new_tokens.append(next_)  # noqa

    return token_utils.untokenize(new_tokens)


def source_init():
    """Adds required imports and function redefinitions"""
    import_fraction = "from fractions import Fraction\n"
    return import_fraction


def add_hook(**_kwargs):
    """Creates and automatically adds the import hook in sys.meta_path"""
    hook = import_hook.create_hook(
        hook_name=__name__,
        source_init=source_init,
        transform_source=transform_source,
    )
    return hook
