"""lambda_encoding.py
------------------------

This codec replaces any Python identifier (token) represented by the
single Greek letter 'λ' by the corresponding string 'lambda' which is
the Python keyword.

The source is assumed to be actually encoded in utf-8.
"""

import codecs
import encodings

from . import console

utf8 = encodings.search_function("utf8")


def register_encoding(encoding_name=None, transform_source=None, hook_name=None):
    if encoding_name is None:
        raise TypeError("You must supply a name for your encoding")
    if transform_source is None or not callable(transform_source):
        raise TypeError("You must supply a function as a source transformation.")

    def ideas_decode(input, errors="strict"):
        """Decodes the source as utf8 and use ``transform_source`` to
        perform the required source transformation.
        """
        text, length = utf8.decode(input, errors)
        text = transform_source(text)
        return text, length

    class CustomIncrementalDecoder(encodings.utf_8.IncrementalDecoder):
        def decode(self, input, final=False):
            self.buffer += input
            if final:
                buff = self.buffer
                self.buffer = b""
                text, _ = ideas_decode(buff)
                buff = text.encode("utf-8")
                return super().decode(buff, final=True)
            else:
                return ""

    def search_function(encoding):
        if encoding != encoding_name:
            return None

        return codecs.CodecInfo(
            name=encoding_name,
            encode=utf8.encode,
            decode=ideas_decode,
            incrementalencoder=utf8.incrementalencoder,
            incrementaldecoder=CustomIncrementalDecoder,
            streamreader=encodings.utf_8.StreamReader,
            streamwriter=utf8.streamwriter,
        )

    codecs.register(search_function)
    print(f"{encoding_name} has been registered.")

    if hook_name is not None:
        transform_source.hook_name = hook_name
    console.configure(transform_source=transform_source)
