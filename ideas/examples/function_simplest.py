"""function_simplest.py
-------------------------

This module enables someone to use ``function`` as a keyword
equivalent to ``lambda``.
"""
from ideas import import_hook
import token_utils


def transform_source(source, **_kwargs):
    """A simple replacement of ``function`` by ``lambda``."""
    tokens = token_utils.tokenize(source)
    for token in tokens:
        if token == "λ":
            token.string = "lambda"
    return token_utils.untokenize(tokens)


def add_hook(**_kwargs):
    """Creates and automatically adds the import hook in sys.meta_path"""
    hook = import_hook.create_hook(transform_source=transform_source)
    return hook
