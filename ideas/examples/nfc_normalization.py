"""Python does 'NFKC normalization' of unicode names by default.
As a result, some different unicode names can end up representing
the same object.

This example demonstrates what could happen if we used
'NFC' normalization instead.

Adapted from unnormalized_unicode which was an
original idea from Sergey B. Kirpichev and is found as
anoter example.
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
            nkfc_name = unicodedata.normalize("NFKC", token_string)
            nfc_name = unicodedata.normalize("NFC", token_string)
            if nkfc_name != nfc_name:
                if token_string not in _NAMES_MAP:
                    _NAMES_MAP[token_string] = f"{nkfc_name}_{uuid.uuid4().hex!s}"
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
        names = [name.replace(v, k) for name in names]
    return sorted(names)


def source_init():
    return """true_dir = dir
from ideas.examples.nfc_normalization import new_dir as dir
"""


def add_hook(**_kwargs):
    """Creates and automatically adds the import hook in sys.meta_path"""
    return import_hook.create_hook(
        transform_source=transform_source, source_init=source_init, hook_name=__name__
    )
