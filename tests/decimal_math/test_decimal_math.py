from ideas import remove_hook, ideas_state
from ideas.included import decimal_math
import codecs
import sys


def test_import_with_hook():
    hook = decimal_math.add_hook()
    from . import use_hook  # noqa

    remove_hook(hook)


def test_import_with_encoding():
    decimal_math.register()
    from . import use_encoding  # noqa

    if sys.version_info >= (3, 10):
        codecs.unregister(ideas_state._codecs_search_functions["decimal_math"])
    del ideas_state._codecs_search_functions["decimal_math"]
