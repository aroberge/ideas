from ideas.import_hook import remove_hook
from ideas.examples import decimal_math


def test_import_with_hook():
    hook = decimal_math.add_hook()
    try:
        import use_hook  # for testing only this file
    except ImportError:
        from . import use_hook  # for testing as part of a suite with pytest
    remove_hook(hook)


def test_import_with_encoding():
    decimal_math.register(add_init=True)
    try:
        import use_encoding  # for testing only this file
    except ImportError:
        from . import use_encoding  # for testing as part of a suite with pytest


if __name__ == '__main__':
    test_import_with_hook()
    test_import_with_encoding()
    print("Done")
