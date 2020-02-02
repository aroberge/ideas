"""This module enables someone to use ``function`` as a keyword
   equivalent to ``lambda``.
"""

import sys

from ideas import import_hook, utils


def transform_source(source, **kwargs):
    """A simple replacement of ``function`` by ``lambda``."""
    new_tokens = []

    for token in utils.tokenize_source(source):
        if token == "function":  # equivalent to token.string == "function"
            token.string = "lambda"
        new_tokens.append(token)

    return utils.untokenize(new_tokens)


def add_hook():
    """Creates and adds the import hook in sys.meta_path"""
    hook = import_hook.create_hook(transform_source=transform_source)
    sys.meta_path.insert(0, hook)
    return hook
