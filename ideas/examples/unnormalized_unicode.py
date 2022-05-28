"""Python does 'normalization' of unicode names by default.
As a result, some different unicode names can end up representing
the same object.

This example demonstrates how different names can be prevented
from being 'normalized'.

Original idea from Sergey B. Kirpichev.
See https://github.com/aroberge/ideas/issues/13 for a reference.
"""
import io
import tokenize
import token_utils
import unicodedata
import uuid

from ideas import import_hook

_NAMES_MAP = {}


def transform_source(source, **_kwargs):
    """Transform names that would normally be 'normalized' by
    Python into different and unique variable names.
    """
    # We want to be able to identify when the source has been modified
    # in case session.config.show_changes has been set to True.
    # However, Python's tokenize module cannot untokenize faithfully:
    # some spaces might be messed up.
    # On the other hand, token_utils can untokenize perfectly, recovering
    # the original source. Unfortunately for this case, it works
    # with (already normalized) strings.
    # So, we combine the two here, just to ensure that we can
    # correctly identify later when a source has been modified.

    new_strings = []
    done_normalization = False
    g = tokenize.tokenize(io.BytesIO(source.encode()).readline)
    for token_type, token_string, _, _, _ in g:
        if token_type == tokenize.NAME:
            normalized_name = unicodedata.normalize("NFKC", token_string)
            if normalized_name != token_string:
                if token_string not in _NAMES_MAP:
                    _NAMES_MAP[token_string] = f"{normalized_name}_{uuid.uuid4().hex!s}"
                new_strings.append(_NAMES_MAP[token_string])
                done_normalization = True
            else:
                new_strings.append(token_string)
    if not done_normalization:
        return source

    new_tokens = []
    tokens = token_utils.tokenize(source)
    for token in tokens:
        if token.is_name():
            token.string = new_strings.pop(0)
        new_tokens.append(token)
    return token_utils.untokenize(new_tokens)


def new_dir(obj=None):
    """Similar to Python's dir, but shows the original name
    entered, not the transformed one.

    Note: the real Python dir() should be available as true_dir().
    """
    import inspect

    if obj is not None:
        names = dir(obj)
    else:
        names = list(inspect.currentframe().f_back.f_locals)
    for k, v in _NAMES_MAP.items():
        names = [
            name.replace(v, k)
            for name in names
            if not (name.startswith("__") and name.endswith("__"))
        ]
    return sorted(names)


true_dir = dir


def source_init():
    name = "ideas.examples.unnormalized_unicode"
    return f"""from {name} import true_dir
from {name} import new_dir as dir
"""


def add_hook(**_kwargs):
    """Creates and automatically adds the import hook in sys.meta_path"""
    return import_hook.create_hook(
        transform_source=transform_source, source_init=source_init, hook_name=__name__
    )
