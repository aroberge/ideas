"""switch.py
-----------------

Implements something similar to version 1.B of
`PEP 3103 <https://www.python.org/dev/peps/pep-3103>`_
"""
from ideas import import_hook, utils
import token_utils


def transform_source(source, callback_params=None, **_kwargs):
    """Replaces code like::

        switch EXPR:
            case EXPR_1:
                SUITE
            case EXPR_2:
                SUITE
            case in EXPR_3, EXPR_4, ...:
                SUITE
            ...
            else:
                SUITE

    by::

        var_name = EXPR
        if var_name == EXPR_1:
                SUITE
        elif var_name == EXPR_2:
                SUITE
        elif var_name in EXPR_3, EXPR_4, ...:
                SUITE
        else:
                SUITE
        del var_name

    Limitation: switch blocks cannot be part of a SUITE of another switch block.
    """
    if callback_params is None or "predictable_names" not in callback_params:
        predictable_names = False
    else:
        predictable_names = callback_params["predictable_names"]
    new_tokens = []
    switch_block = False
    first_case = False
    if predictable_names:
        variable_name = utils.generate_predictable_names()
    else:
        variable_name = utils.generate_variable_names()

    for line in token_utils.get_lines(source):
        first_token = token_utils.get_first(line)
        if first_token is None:
            new_tokens.extend(line)
            continue

        if len(line) > 1:
            _index = token_utils.get_first_index(line)
            second_token = line[_index + 1]
        else:
            second_token = None

        if not switch_block:
            if first_token == "switch":
                switch_indent = first_token.start_col
                var_name = next(variable_name)
                first_token.string = f"{var_name} ="
                switch_block = True
                first_case = True
                colon = token_utils.get_last(line)
                colon.string = ""
        else:
            if first_token.start_col == switch_indent:
                switch_block = False
                new_tokens.extend([" " * switch_indent + f"del {var_name}\n"])

            elif first_token == "case" or first_token == "else":
                if first_case and first_token == "case":
                    if second_token == "in":
                        first_token.string = f"if {var_name}"
                    else:
                        first_token.string = f"if {var_name} =="
                    first_case = False
                elif first_token == "case":
                    if second_token == "in":
                        first_token.string = f"elif {var_name}"
                    else:
                        first_token.string = f"elif {var_name} =="
                dedent = first_token.start_col - switch_indent
                line = token_utils.dedent(line, dedent)

        new_tokens.extend(line)
    return token_utils.untokenize(new_tokens)


def add_hook(
    predictable_names=False,
    **_kwargs,
):
    """Creates and adds the import hook in sys.meta_path"""
    callback_params = {"predictable_names": predictable_names}
    hook = import_hook.create_hook(
        transform_source=transform_source,
        callback_params=callback_params,
        hook_name=__name__,
    )
    return hook
