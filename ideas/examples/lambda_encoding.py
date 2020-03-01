"""lambda_encoding.py
------------------------

This codec replaces any Python identifier (token) represented by the
single Greek letter 'λ' by the corresponding string 'lambda' which is
the Python keyword.

The source is assumed to be actually encoded in utf-8.
"""

import codecs
import encodings
from ideas import console
import token_utils


utf8 = encodings.search_function("utf8")


def transform_source(source, **kwargs):
    """Simple transformation: replaces any single token λ by lambda.

    By defining this function, we can also make use of Ideas' console.
    """
    tokens = token_utils.tokenize(source)
    for token in tokens:
        if token == "λ":
            token.string = "lambda"
    return token_utils.untokenize(tokens)


def lambda_decode(input, errors="strict"):
    """Decodes the source as utf8 and use ``transform_source`` to
    perform the required source transformation.
    """
    text, length = utf8.decode(input, errors)
    text = transform_source(text)
    return text, length


class LambdaIncrementalDecoder(encodings.utf_8.IncrementalDecoder):
    def decode(self, input, final=False):
        self.buffer += input
        if final:
            buff = self.buffer
            self.buffer = b""
            text, _ = lambda_decode(buff)
            buff = text.encode("utf-8")
            return super().decode(buff, final=True)
        else:
            return ""


def search_function(encoding):
    if encoding != "lambda-encoding":
        return None

    return codecs.CodecInfo(
        name="lambda-encoding",
        encode=utf8.encode,
        decode=lambda_decode,
        incrementalencoder=utf8.incrementalencoder,
        incrementaldecoder=LambdaIncrementalDecoder,
        streamreader=encodings.utf_8.StreamReader,
        streamwriter=utf8.streamwriter,
    )


codecs.register(search_function)


def enable_console():
    transform_source._hook_name_ = __name__
    console.configure(transform_source=transform_source)
