# my_function_keyword.py

from ideas import import_hook
import token_utils


def do_transform(source):  # extracted for clarity
    new_tokens = []
    for token in token_utils.tokenize(source):
        if token == "function":
            token.string = "lambda"
        new_tokens.append(token)
    return token_utils.untokenize(new_tokens)


def transform_source(source, callback_params=None, **kwargs):
    if callback_params is not None:
        if callback_params["show_original"]:
            print("-------Original-------")
            print(source)
            print("----------------------")

    new_source = do_transform(source)

    if callback_params is not None:
        if callback_params["show_changes"]:
            print("--------New-----------")
            print(new_source)
            print("----------------------")
    return new_source


def add_hook(show_original=False, show_changes=False):
    callback_params = {
        "show_original": show_original,
        "show_changes": show_changes,
    }
    hook = import_hook.create_hook(
        transform_source=transform_source,
        callback_params=callback_params,
        name=__name__,
    )
    return hook
