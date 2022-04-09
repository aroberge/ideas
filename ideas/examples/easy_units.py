"""
implicit_multiplication.py
---------------------------

This module is intended to demonstrate some unusual transformations
to allow someone to write equations as they would on paper
and have Python interpret them properly.
"""
from ideas import import_hook, utils
import token_utils

PREFIX = ""


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
    global PREFIX
    lines = source.split("\n")
    for line in lines:
        line = line.replace(" ", "").replace("\n", "")
        if line.endswith("=pint.UnitRegistry()"):
            PREFIX = line.split("=pint.UnitRegistry")[0] + "."
        elif line.endswith("=UnitRegistry()"):
            PREFIX = line.split("=UnitRegistry()")[0] + "."

    original = source
    if callback_params["show_original"]:
        utils.print_source(source, "Original")

    source = transform_units(source)

    if callback_params["show_transformed"] and original != source:
        utils.print_source(source, "Transformed")
    

    return source


def transform_units(source):
    tokens = token_utils.tokenize(source)
    if not tokens:
        return source

    converting_units = False
    dividing_by_units = False
    prev_token = tokens[0]
    new_tokens = [prev_token]
    prev_is_number = False
    prev_is_identifier = False

    for token in tokens[1:]:
        # Take note of the token type before possibly changing its content
        is_identifier = token.is_identifier()
        is_number = token.is_number()

        if converting_units and PREFIX and is_identifier:
            token.string = PREFIX + token.string

        if converting_units and token == "]":
            converting_units = False
            if dividing_by_units:
                token.string = ")"
                dividing_by_units = False
            else:
                token.string = ""

        elif prev_is_number and token == "[":
            converting_units = True
            token.string = " * "

        elif converting_units and token == "/":
            dividing_by_units = True
            token.string ="/("

        elif converting_units and is_identifier and (prev_is_number or prev_is_identifier):
            token.string = " * " + token.string

        elif converting_units and token == "^":
            token.string = "**"

        new_tokens.append(token)
        prev_token = token
        prev_is_number = is_number
        prev_is_identifier = is_identifier
    
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
