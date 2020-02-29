"""
implicit_multiplication.py
---------------------------

This module is intended to demonstrate some unusual transformations
to allow someone to write equations as they would on paper
and have Python interpret them properly.
"""
from ideas import import_hook, token_utils, utils


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
    """In Python, having a ``NUMBER`` followed by a ``NAME`` or a ``(``
    is a syntax error.  So, we treat those cases as though they indicate
    that a multiplication is implied.
    """
    new_tokens = []

    lines = token_utils.get_lines(source)
    for line in lines:
        multiply_by_number(line)
        multiply_two_identifiers(line)
        new_tokens.extend(line)

    return token_utils.untokenize(new_tokens)


def multiply_by_number(line):
    """In Python, having a ``NUMBER`` followed by a ``NAME`` or a ``(``
    or another ``NUMBER`` is a syntax error.
    The following transformation identifies such
    cases and inserts a multiplication symbol between ``NUMBER`` and
    the next token.
    """

    for token, next_token in token_utils.get_pairs(line):
        if token.is_number() and (
            next_token.is_identifier() or next_token == "(" or next_token.is_number()
        ):
            token.string = token.string + " * "


def multiply_two_identifiers(line):
    """In Python, having an identifier followed by another identifier,
    where neither identifier is a keyword, is a syntax error.
    The following transformation identifies such
    cases and inserts a multiplication symbol between the two identifiers.
    """
    for token, next_token in token_utils.get_pairs(line):
        if token.is_identifier() and next_token.is_identifier():
            token.string = token.string + " *"


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
