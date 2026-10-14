# test_lambda_encoding.py

import codecs
from ideas import ideas_state


def test_import():
    # The following import will automatically register a codec
    from ideas.included import lambda_codec  # noqa
    from . import short_program  # noqa

    for fn in ideas_state._codecs_search_functions:
        codecs.unregister(fn)


if __name__ == "__main__":
    import short_program
