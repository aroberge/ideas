"""
Fractional math (token based)
=============================

.. admonition:: Summary

   This is includes a source transformation that converts
   integers literals that are followed by the ``/`` operator
   into instances of the Fraction class in the source using the tokenizer.

   In a later section, we do something similar but using an
   Abstract Syntax Tree (AST) transformation, which is a more robust
   approach for this type of example.

Consider the following standard Python code::

    >>> x = 1/10
    >>> for i in range(11):
    ...    print(i * x)
    ...
    0.0
    0.1
    0.2
    0.30000000000000004
    0.4
    0.5
    0.6000000000000001
    0.7000000000000001
    0.8
    0.9
    1.0

This is quite surprising for beginners, not familiar with the
limitations of representing floating point numbers.

However, we can "fix" this using an import hook that wraps
integer, which are followed by a ``/``, into a ``Fraction`` instance::

    > python -m ideas -a fractions_tok
       The following initializing code from ideas is included:

    from fractions import Fraction

    Ideas Console version 0.0.38. [Python version: 3.7.9]

    ideas> x =  1 / 10

    ideas> for i in range(11):
      ...     print(i * x)
      ...
    0
    1/10
    1/5
    3/10
    2/5
    1/2
    3/5
    7/10
    4/5
    9/10
    1

    ideas> from ideas.session import config

    ideas> config.show_changes = True

    ideas> x = 1 / 10
    new: x = Fraction(1) / 10

    ideas>

This example was created after a similar example using AST transformation
was created as a proof of concept. For more details about the
difference, please have a look at the AST-based example.
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
