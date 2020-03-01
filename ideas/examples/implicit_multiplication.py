"""
implicit_multiplication.py
---------------------------

This module is intended to demonstrate some unusual transformations
to allow someone to write equations as they would on paper
and have Python interpret them properly.
"""
from ideas import import_hook, utils
import token_utils


def transform_source(source, callback_params=None, **kwargs):
    """This function is called by the import hook loader with the named keyword
       that we specified when we created the import hook.

       It gives us the option to compare the original source and the transformed
       one. This type of additional option can be useful when debugging
       a source transformer. Furthermore, if we wish to define a source
       transformation that combines the effect of multiple existing
       transformations, we can combine the existing "inner" functions to
       create our new transformation.
    """
    if callback_params["show_original"]:
        utils.print_source(source, "Original")

    source = add_multiplication_symbol(source)

    if callback_params["show_transformed"]:
        utils.print_source(source, "Transformed")

    return source


def add_multiplication_symbol(source):
    """This adds a multiplication symbol where it would be understood as
    being implicit by the normal way algebraic equations are written but would
    be a SyntaxError in Python. Thus we have::

        2n  -> 2*n
        n 2 -> n* 2
        2(a+b) -> 2*(a+b)
        (a+b)2 -> (a+b)*2
        2 3 -> 2* 3
        m n -> m* n
        (a+b)c -> (a+b)*c

    The obvious one (in algebra) being left out is something like ``n(...)``
    which is a function call - and thus valid Python syntax.
    """

    tokens = token_utils.tokenize(source)
    if not tokens:
        return tokens

    prev_token = tokens[0]
    new_tokens = [prev_token]

    for token in tokens[1:]:
        # The code has been written in a way to demonstrate that this type of
        # transformation could be done as the source is tokenized by Python.
        if (
            (
                prev_token.is_number()
                and (token.is_identifier() or token.is_number() or token == "(")
            )
            or (
                prev_token.is_identifier()
                and (token.is_identifier() or token.is_number())
            )
            or (prev_token == ")" and (token.is_identifier() or token.is_number()))
        ):
            new_tokens.append("*")
        new_tokens.append(token)
        prev_token = token

    return token_utils.untokenize(new_tokens)


def add_hook(show_original=False, show_transformed=False, verbose_finder=False):
    """Creates and automatically adds the import hook in sys.meta_path"""
    callback_params = {
        "show_original": show_original,
        "show_transformed": show_transformed,
    }
    hook = import_hook.create_hook(
        transform_source=transform_source,
        callback_params=callback_params,
        hook_name=__name__,
        verbose_finder=verbose_finder,
    )
    return hook
