"""nobreak.py
-------------

This module enables someone to use ``nobreak`` as a keyword
   equivalent to ``else`` in ``for`` and ``while`` loops.

"""
from ideas import import_hook, utils
import token_utils


def transform_source(source, callback_params=None, **_kwargs):
    """This function is called by the import hook loader with the named keyword
    that we specified when we created the import hook.

    It gives us the option to compare the original source and the transformed
    one. This type of additional option can be useful when debugging
    a source transformer. Furthermore, if we wish to define a source
    transformation that combines the effect of multiple existing
    transformations, we can combine the existing "inner" functions to
    create our new transformation.
    """
    if callback_params["show_original"]:
        utils.print_source(source, "Original")

    source = nobreak_as_a_keyword(source)

    if callback_params["show_transformed"]:
        utils.print_source(source, "New")
    return source


def nobreak_as_a_keyword(source):
    """``nobreak`` is replaced by ``else`` only if it is the first
    non-space token on a line and if its indentation matches
    that of a ``for`` or ``while`` block.
    """
    indentations = {}
    lines = token_utils.get_lines(source)
    new_tokens = []
    for line in lines:
        first = token_utils.get_first(line)
        if first is None:
            new_tokens.extend(line)
            continue
        if first == "nobreak":
            if first.start_col in indentations:
                if indentations[first.start_col] in ["for", "while"]:
                    first.string = "else"
        indentations[first.start_col] = first.string
        new_tokens.extend(line)

    return token_utils.untokenize(new_tokens)


def add_hook(
    show_original=False, show_transformed=False, verbose_finder=False, **_kwargs
):
    """Creates and automatically adds the import hook in sys.meta_path"""
    callback_params = {
        "show_original": show_original,
        "show_transformed": show_transformed,
    }
    hook = import_hook.create_hook(
        transform_source=transform_source,
        callback_params=callback_params,
        hook_name=__name__,
        verbose_finder=verbose_finder,
    )
    return hook
