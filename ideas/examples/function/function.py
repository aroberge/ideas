import sys

from ideas import import_hook, utils


def print_info(kind, source):
    print(f"==========={kind}============")
    print(source)
    print("-----------------------------")


def transform_source(source, show_original=False, show_transformed=False, **kwargs):
    if show_original:
        print_info("Original", source)

    source = function_as_a_keyword(source)

    if show_transformed:
        print_info("Transformed", source)
    return source


def function_as_a_keyword(source):
    """A simple replacement of ``function`` by ``lambda``.

    Note that, while the string ``lambda`` is shorter than ``function``, we
    do not adjust the information (start_col, end_col) about the position
    of the token. ``untokenize`` uses that information together with the
    information about each original line, to properly keep track of the
    spacing between tokens.
    """
    new_tokens = []
    for token in utils.tokenize_source(source):
        if token.string == "function":
            token.string = "lambda"
        new_tokens.append(token)

    new_source = utils.untokenize(new_tokens)
    return new_source


def add_hook(show_original=False, show_transformed=False):
    """Creates and adds the import hook in sys.meta_path"""
    callback_params = {
        "show_original": show_original,
        "show_transformed": show_transformed,
    }
    hook = import_hook.create_hook(
        transform_source=transform_source, callback_params=callback_params
    )
    sys.meta_path.insert(0, hook)
    return hook


def tear_down(hook, module):  # for testing
    """Useful for testing and isolating import hooks"""
    import_hook.remove_hook(hook)
    del sys.modules[module.__name__]
