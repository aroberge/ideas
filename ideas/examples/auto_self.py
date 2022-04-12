"""auto_self.py
-----------------

Helps to reduce the amount of typing required and increases readability
when assigning attributes in a class's ``__init__()`` method.
"""
from ideas import import_hook, utils
import token_utils


def transform_source(source, callback_params=None, **_kwargs):
    """This function is called by the import hook loader and is used as a
    wrapper for the function where the real transformation is performed.
    """
    if callback_params["show_original"]:
        utils.print_source(source, "Original")

    source = automatic_self(source)

    if callback_params["show_transformed"]:
        utils.print_source(source, "New")

    return source


def automatic_self(source):
    """Replaces code like::

        self .= :
            a
            b
            c = this if __ == that else ___

    by::

        self.a = a
        self.b = b
        self.c = this if c == that else c
    """
    new_tokens = []
    auto_self_block = False
    self_name = ""
    indentation = 0

    get_nb = token_utils.get_number
    get_first = token_utils.get_first
    get_first_index = token_utils.get_first_index

    for tokens in token_utils.get_lines(source):
        if auto_self_block:
            variable = get_first(tokens)
            if variable is not None:  # None would mean an empty line
                var_name = variable.string
                block_indent = variable.start_col
                if block_indent > indentation:
                    dedent = block_indent - indentation
                    if get_nb(tokens) == 1:
                        variable.string = f"{self_name}.{var_name} = {var_name}"
                        tokens = token_utils.dedent(tokens, dedent)
                    else:
                        variable.string = f"{self_name}.{var_name}"
                        for token in tokens:
                            if token.string == "__":
                                token.string = var_name
                        tokens = token_utils.dedent(tokens, dedent)
                else:
                    auto_self_block = False
        elif get_nb(tokens) == 4:
            index = get_first_index(tokens)
            if (
                tokens[index].is_identifier()
                and tokens[index + 1] == "."
                and tokens[index + 2] == "="
                and tokens[index + 1].end_col == tokens[index + 2].start_col
                and tokens[index + 3] == ":"
            ):
                self_name = tokens[index].string
                indentation = tokens[index].start_col
                auto_self_block = True
                continue
        new_tokens.extend(tokens)
    return token_utils.untokenize(new_tokens)


def add_hook(
    show_original=False, show_transformed=False, verbose_finder=False, **_kwargs
):
    """Creates and adds the import hook in sys.meta_path"""
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
