import sys

from ideas import import_hook, utils


def transform_source(source, show_original=False, show_transformed=False, **kwargs):
    if show_original:
        print("===== Original ====")
        print(source)
        print("-" * 50)

    source = function_as_a_keyword(source)

    if show_transformed:
        print("===== transformed ====")
        print(source)
        print("-" * 50)

    return source


def function_as_a_keyword(source):
    """We simply replace 'function' by 'lambda'.
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
        source_transformer=transform_source, callback_params=callback_params
    )
    sys.meta_path.insert(0, hook)
    return hook


def tear_down(hook, module):  # for testing
    """Useful for testing and isolating import hooks"""
    import_hook.remove_hook(hook)
    del sys.modules[module.__name__]
