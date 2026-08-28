"""This module enables someone to use ``function`` as a keyword
equivalent to ``lambda``.
"""

from ideas import create_hook
import token_utils


def transform_source(source, **_kwargs):
    """This performs a simple replacement of ``function`` by ``lambda``."""
    new_tokens = []
    for token in token_utils.tokenize(source):
        # token_utils allows us to easily replace the string content
        # of any token
        if token == "function":
            token.string = "lambda"
        new_tokens.append(token)

    return token_utils.untokenize(new_tokens)


def add_hook():
    """Creates and automatically adds the import hook in sys.meta_path"""
    hook = create_hook(transform_source=transform_source, name=__name__)
    return hook
