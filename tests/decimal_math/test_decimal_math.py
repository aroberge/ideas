from ideas import remove_hook, ideas_state
from ideas.included import decimal_math
import codecs


def test_import_with_hook():
    hook = decimal_math.add_hook()
    from . import use_hook  # noqa

    remove_hook(hook)


def test_import_with_encoding():
    decimal_math.register()
    from . import use_encoding  # noqa

    for fn in ideas_state._codecs_search_functions:
        codecs.unregister(fn)
