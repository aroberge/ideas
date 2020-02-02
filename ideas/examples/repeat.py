"""Adds ``repeat`` as a keyword to write simple loops that repeat
a set number of times.  That is:

    repeat 3:
        a = 2
        repeat a*a:
            pass

is equivalent to

    for random_variable_name_1 in range(3):
        a = 2
        for random_variable_name_2 in range(a*a):
            pass
"""

import sys
import uuid

from ideas import import_hook, utils


class RepeatSyntaxError(Exception):
    """Currently, only raised when a repeat statement has a missing colon"""

    pass


def generate_variable_names():
    """Generator that yields random variable names"""
    while True:
        name = uuid.uuid4()
        yield "_%s" % name.hex


def generate_predictable_names():
    n = 0
    while True:
        n += 1
        yield "_%s" % n


def print_info(kind, source):
    """prints information about the source - either original or transformed"""
    print(f"==========={kind}============")
    print(source)
    print("-----------------------------")


def transform_source(
    source,
    show_original=False,
    show_transformed=False,
    predictable_names=False,
    **kwargs,
):
    """This function is called by the import hook loader with the named keyword
       that we specified when we created the import hook.

       It gives us the option to compare the original source and the transformed
       one. This type of additional option can be useful when debugging
       a source transformer. Once such options are added, there are essentially
       no advantage in removing them as the next programmer who wishes to
       build upon this example will likely find this useful.
    """
    if show_original:
        print_info("Original", source)

    source = convert_repeat(source, predictable_names=predictable_names)

    if show_transformed:
        print_info("Transformed", source)
    return source


def convert_repeat(source, predictable_names=False):
    """Replaces instances of

        repeat ... : # optional comment
    by

        for random_variable_name in range( ... ): # optional comment


    A complete repeat statement is restricted to be on a single line
    """

    new_tokens = []
    if predictable_names:
        variable_name = generate_predictable_names()
    else:
        variable_name = generate_variable_names()

    for tokens in utils.get_lines_of_tokens(source):
        # a line of tokens can start with DEDENT tokens ...
        index = utils.get_first_nonspace_token_index(tokens)
        first_token = tokens[index]
        if first_token == "repeat":
            colon_position = -1
            # Note: a newline token string could be either "" or "\n"
            if tokens[colon_position].is_newline():
                colon_position -= 1
            if tokens[colon_position].is_comment():
                colon_position -= 1
            colon = tokens[colon_position]
            if colon != ":":
                raise RepeatSyntaxError(
                    "Missing colon for repeat statement on line "
                    + f"{first_token.start_row}\n    {first_token.line}."
                )

            first_token.string = "for %s in range(" % next(variable_name)
            colon.string = "):"

        new_tokens.extend(tokens)

    return utils.untokenize(new_tokens)


def add_hook(show_original=False, show_transformed=False, predictable_names=False):
    """Creates and adds the import hook in sys.meta_path"""
    callback_params = {
        "show_original": show_original,
        "show_transformed": show_transformed,
        "predictable_names": predictable_names,
    }
    hook = import_hook.create_hook(
        transform_source=transform_source, callback_params=callback_params
    )
    sys.meta_path.insert(0, hook)
    return hook
