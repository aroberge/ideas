"""
This module enables someone to use ``nobreak`` as a keyword
equivalent to ``else`` in ``for`` and ``while`` loops.
"""
from ideas import import_hook
import token_utils


def transform_source(source, **_kwargs):
    """``nobreak`` is replaced by ``else`` only if it is the first
    non-space token on a line and if its indentation matches
    that of a ``for`` or ``while`` block.
    """
    indentations = {}
    lines = token_utils.get_lines(source)
    new_tokens = []
    # The following is not a proper parser, but it should work
    # well enough in most cases, for well-formatted code.
    for line in lines:
        first = token_utils.get_first(line)
        if first is None:
            new_tokens.extend(line)
            continue
        if first == "nobreak":
            if first.start_col in indentations:
                if indentations[first.start_col] in ["for", "while"]:
                    first.string = "else"
                    del indentations[first.start_col]
        indentations[first.start_col] = first.string
        new_tokens.extend(line)

    return token_utils.untokenize(new_tokens)


def add_hook(**_kwargs):
    """Creates and automatically adds the import hook in sys.meta_path"""
    return import_hook.create_hook(
        transform_source=transform_source,
        hook_name=__name__,
    )
