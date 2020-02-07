"""function_simplest.py

This module enables someone to use ``function`` as a keyword
equivalent to ``lambda``.
"""
from ideas import import_hook, token_utils


def transform_source(source, **kwargs):
    """A simple replacement of ``function`` by ``lambda``."""
    new_tokens = []

    for token in token_utils.tokenize_source(source):
        if token == "function":  # equivalent to token.string == "function"
            token.string = "lambda"
        new_tokens.append(token)

    return token_utils.untokenize(new_tokens)


def add_hook():
    """Creates and automatically adds the import hook in sys.meta_path"""
    hook = import_hook.create_hook(transform_source=transform_source)
    return hook
