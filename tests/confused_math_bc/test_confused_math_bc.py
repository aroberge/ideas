import pytest
import sys

from ideas.examples import confused_math_bc
from ideas.import_hook import remove_hook


@pytest.mark.skipif(sys.version_info.minor != 7, reason="requires python 3.7")
def test_simple_case():
    hook = confused_math_bc.add_hook()

    try:
        import confused_math  # for testing only this file
    except (ImportError, ModuleNotFoundError):
        from . import confused_math  # for testing as part of a suite with pytest
    remove_hook(hook)


if __name__ == "__main__":
    test_simple_case()
    print("success")
