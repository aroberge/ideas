"""switch.py
-----------------

Implements version 1.B of `PEP 3103 <https://www.python.org/dev/peps/pep-3103>`_
"""
import uuid

from ideas import import_hook, token_utils, utils


def generate_variable_names():
    """Generator that yields random variable names"""
    while True:
        name = uuid.uuid4()
        yield "_%s" % name.hex


def generate_predictable_names():
    """Generator that yields predictable variable names - useful for testing"""
    n = 0
    while True:
        n += 1
        yield "_%s" % n


def transform_source(source, callback_params=None, **kwargs):
    """This function is called by the import hook loader and is used as a
    wrapper for the function where the real transformation is performed.
    """
    if callback_params["show_original"]:
        utils.print_source(source, "Original")

    source = convert_switch(
        source, predictable_names=callback_params["predictable_names"]
    )

    if callback_params["show_transformed"]:
        utils.print_source(source, "Transformed")

    return source


def convert_switch(source, predictable_names=False):
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
    new_tokens = []
    switch_block = False
    first_case = False
    if predictable_names:
        variable_name = generate_predictable_names()
    else:
        variable_name = generate_variable_names()

    for line in token_utils.get_lines(source):
        first_token = token_utils.get_first(line)
        if first_token is None:
            new_tokens.extend(line)
            continue
        first_token_index = token_utils.get_first_index(line)
        second_token = line[first_token_index + 1]

        if switch_block:
            if first_token.start_col == switch_indent:  # noqa
                switch_block = False
                new_tokens.extend([" " * switch_indent + f"del {var_name}\n"])  # noqa

            elif first_token == "case" or first_token == "else":
                if first_case and first_token == "case":
                    if second_token == "in":
                        first_token.string = f"if {var_name}"  # noqa
                    else:
                        first_token.string = f"if {var_name} =="  # noqa
                    first_case = False
                elif first_token == "case":
                    if second_token == "in":
                        first_token.string = f"elif {var_name}"  # noqa
                    else:
                        first_token.string = f"elif {var_name} =="  # noqa
                dedent = first_token.start_col - switch_indent  # noqa
                line = token_utils.dedent(line, dedent)

        elif first_token == "switch":
            switch_indent = first_token.start_col  # noqa
            var_name = next(variable_name)
            first_token.string = f"{var_name} ="
            switch_block = True
            first_case = True
            colon = token_utils.get_last(line)
            colon.string = ""

        new_tokens.extend(line)
    return token_utils.untokenize(new_tokens)


def add_hook(
    show_original=False,
    show_transformed=False,
    predictable_names=False,
    verbose_finder=False,
):
    """Creates and adds the import hook in sys.meta_path"""
    callback_params = {
        "show_original": show_original,
        "show_transformed": show_transformed,
        "predictable_names": predictable_names,
    }
    hook = import_hook.create_hook(
        transform_source=transform_source,
        callback_params=callback_params,
        hook_name=__name__,
        verbose_finder=verbose_finder,
    )
    return hook
