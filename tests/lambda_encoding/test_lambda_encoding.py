# test_lambda_encoding.py

import codecs
import sys
from ideas import ideas_state


def test_import():
    # The following import will automatically register a codec
    from ideas.included import lambda_codec  # noqa
    from . import short_program  # noqa

    if sys.version_info >= (3, 10):
        codecs.unregister(ideas_state._codecs_search_functions["lambda_encoding"])
    del ideas_state._codecs_search_functions["lambda_encoding"]


if __name__ == "__main__":
    import short_program
