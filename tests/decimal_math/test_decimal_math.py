from ideas.import_hook import remove_hook
from ideas.examples import decimal_math
import sys
import pytest


def test_import_with_hook():
    hook = decimal_math.add_hook()
    try:
        from . import use_hook  # for testing as part of a suite with pytest
    except ImportError:
        import use_hook  # for testing only this file
    remove_hook(hook)


@pytest.mark.skipif(sys.version_info.minor not in (6, 7, 8),
                    reason="requires python 3.6, 3.7 or 3.8")
def test_import_with_encoding():
    decimal_math.register()
    try:
        import use_encoding  # for testing only this file
    except ImportError:
        from . import use_encoding  # for testing as part of a suite with pytest


if __name__ == "__main__":
    test_import_with_hook()
    test_import_with_encoding()
    print("Done")
