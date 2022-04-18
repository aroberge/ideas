from ideas.import_hook import remove_hook
from ideas.examples import decimal_math


def test_import_with_hook():
    hook = decimal_math.add_hook()
    from . import use_hook  # noqa
    remove_hook(hook)


def test_import_with_encoding():
    decimal_math.register()
    from . import use_encoding  # noqa

