"""
Adds ``repeat`` as a keyword to write loops. The four constructs supported
are::

    repeat n:
        # code

    repeat while condition:
        # code

    repeat until condition:
        # code

    repeat forever:
        # code

For example::

    repeat 3:
        a = 2
        repeat a*a:
            pass

is equivalent to::

    for unique_variable_name_1 in range(3):
        a = 2
        for unique_variable_name_2 in range(a*a):
            pass
"""
from ideas import import_hook, utils
import token_utils


class RepeatSyntaxError(Exception):
    """Currently, only raised when a repeat statement has a missing colon."""

    pass


def transform_source(source, callback_params=None, **_kwargs):
    """This function is called by the import hook loader and is used as a
    wrapper for the function where the real transformation is performed.
    """
    """Replaces instances of::

        repeat forever: -> while True:
        repeat while condition: -> while  condition:
        repeat until condition: -> while not condition:
        repeat n: -> for _uid in range(n):

    A complete repeat statement is restricted to be on a single line ending
    with a colon (optionally followed by a comment). If the colon is
    missing, a ``RepeatSyntaxError`` is raised.
    """
    if callback_params is None or "predictable_names" not in callback_params:
        predictable_names = False
    else:
        predictable_names = callback_params["predictable_names"]
    new_tokens = []
    if predictable_names:
        variable_name = utils.generate_predictable_names()
    else:
        variable_name = utils.generate_variable_names()

    for tokens in token_utils.get_lines(source):
        # a line of tokens can start with INDENT or DEDENT tokens ...
        first_token = token_utils.get_first(tokens)
        if first_token == "repeat":
            last_token = token_utils.get_last(tokens)
            if last_token != ":":
                raise RepeatSyntaxError(
                    "Missing colon for repeat statement on line "
                    + f"{first_token.start_row}\n    {first_token.line}."
                )

            repeat_index = token_utils.get_first_index(tokens)
            second_token = tokens[repeat_index + 1]
            if second_token == "forever":
                first_token.string = "while"
                second_token.string = "True"
            elif second_token == "while":
                first_token.string = "while"
                second_token.string = ""
            elif second_token == "until":
                first_token.string = "while"
                second_token.string = "not"
            else:
                first_token.string = "for %s in range(" % next(variable_name)
                last_token.string = "):"

        new_tokens.extend(tokens)

    return token_utils.untokenize(new_tokens)


def add_hook(predictable_names=False, **_kwargs):
    """Creates and adds the import hook in sys.meta_path"""
    callback_params = {"predictable_names": predictable_names}
    hook = import_hook.create_hook(
        transform_source=transform_source,
        callback_params=callback_params,
        hook_name=__name__,
    )
    return hook
