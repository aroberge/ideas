# The following import will automatically register a codec
from ideas.examples import lambda_codec  # noqa


def test_import():
    try:
        import short_program  # for testing only this file
    except ImportError:
        from . import short_program  # for testing as part of a suite with pytest


if __name__ == '__main__':
    test_import()
