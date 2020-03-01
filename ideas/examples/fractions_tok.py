"""fractions_tok.py
----------------

Converts integers literals into instances of the Fraction class in
the source using the tokenizer.
This works for doing using Python exclusively to do integer arithmetics but it
fails miserably in other contexts that expect ``int``.

It is only meant as an alternative to the AST transformation demo.
"""
from ideas import import_hook
import token_utils


def transform_source(source, **kwargs):
    """Replace integers by Fraction objects"""
    tokens = token_utils.tokenize(source)
    for token in tokens:
        if token.is_integer():
            token.string = f"Fraction({token.string})"

    return token_utils.untokenize(tokens)


new_range = """
old_range = range
def range(n, *args):
    if len(args) == 0:
        return old_range(int(n))
    elif len(args) == 1:
        return old_range(int(n), int(args[0]))
    else:
        return old_range(int(n), int(args[0]), int(args[1]))

"""


def source_init():
    """Adds required imports and function redefinitions"""
    import_fraction = "from fractions import Fraction\n"
    return import_fraction + new_range


def add_hook(verbose_finder=False):
    """Creates and automatically adds the import hook in sys.meta_path"""
    hook = import_hook.create_hook(
        hook_name=__name__,
        source_init=source_init,
        transform_source=transform_source,
        verbose_finder=verbose_finder,
    )
    return hook
