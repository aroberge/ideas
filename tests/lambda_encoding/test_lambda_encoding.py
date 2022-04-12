# The following import will automatically register a codec
from ideas.examples import lambda_codec  # noqa
import sys
import pytest


@pytest.mark.skipif(sys.version_info.minor not in (6, 7, 8),
                    reason="requires python 3.6, 3.7 or 3.8")
def test_import():
    try:
        import short_program  # for testing only this file
    except ImportError:
        from . import short_program  # for testing as part of a suite with pytest


if __name__ == "__main__":
    test_import()
