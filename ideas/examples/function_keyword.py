"""
function_keyword.py
-------------------

This module enables someone to use ``function`` as a keyword
   equivalent to ``lambda``.

   It is slightly more complicated than ``function_simplest.py`` as it
   demonstrates how we can pass parameters when adding an import hook;
   these parameters will be passed back to our function
   ``transform_source``.
"""
from ideas import import_hook
import token_utils


def transform_source(source, **_kwargs):
    """A simple replacement of ``function`` by ``lambda``.

    Note that, while the string ``lambda`` is shorter than ``function``, we
    do not adjust the information (start_col, end_col) about the position
    of the token. ``untokenize`` uses that information together with the
    information about each original line, to properly keep track of the
    spacing between tokens.
    """
    new_tokens = []
    for token in token_utils.tokenize(source):
        if token == "function":
            token.string = "lambda"
        new_tokens.append(token)

    return token_utils.untokenize(new_tokens)


def add_hook(**_kwargs):
    """Creates and automatically adds the import hook in sys.meta_path"""
    hook = import_hook.create_hook(
        transform_source=transform_source,
        hook_name=__name__,
    )
    return hook
