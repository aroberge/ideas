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
import unicodedata
import uuid

from ideas import import_hook

_NAMES_MAP = {}


def transform_source(source, **_kwargs):
    """Transform names that would normally be 'normalized' by
    Python into different and unique variable names.
    """
    # Note: we cannot use token_utils as it does the NKFC normalization
    result = []
    g = tokenize.tokenize(io.BytesIO(source.encode()).readline)
    for token_type, token_string, _, _, _ in g:
        if token_type == tokenize.NAME:
            normalized_name = unicodedata.normalize("NFKC", token_string)
            if normalized_name != token_string:
                if token_string not in _NAMES_MAP:
                    _NAMES_MAP[token_string] = f"{normalized_name}_{uuid.uuid4().hex!s}"
                token_string = _NAMES_MAP[token_string]
        result.append((token_type, token_string))
    return tokenize.untokenize(result).decode()


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
        names = [name.replace(v, k) for name in names]
    return sorted(names)


def source_init():
    return """true_dir = dir
from ideas.examples.unnormalized_unicode import new_dir as dir
"""


def add_hook(**_kwargs):
    """Creates and automatically adds the import hook in sys.meta_path"""
    return import_hook.create_hook(
        transform_source=transform_source, source_init=source_init, hook_name=__name__
    )
