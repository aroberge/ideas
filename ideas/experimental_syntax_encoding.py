"""experimental_syntax_encoding.py
----------------------------------

This is just a proof of concept.

The source is assumed to be actually encoded in utf-8.
"""

import codecs
import encodings
import re

from . import console

utf8 = encodings.search_function("utf8")


def transform_source(source, **kwargs):
    """Scans a module for special construct identifying transformers
    to use. Apply each transformer in turn to the original source
    and returns a transformed source.
    """
    modules = []
    transformers = []

    # Scan for special import statements
    pattern = re.compile("from experimental-syntax import (.*)")
    lines = source.split("\n")
    new_lines = []
    for line in lines:
        match = re.search(pattern, line)
        if match:
            module_name = match.group(1).strip()
            module = __import__(module_name)
            new_lines.append(getattr(module, "import_statement"))
            transformers.append(getattr(module, "transform_source"))
        else:
            new_lines.append(line)
    source = "\n".join(new_lines)

    for transform in transformers:
        source = transform(source)
    return source


def register_encoding(encoding_name=None, transform_source=None):
    def experimental_syntax_decode(input, errors="strict"):
        """Decodes the source as utf8 and use ``transform_source`` to
        perform the required source transformation.
        """
        text, length = utf8.decode(input, errors)
        text = transform_source(text)
        return text, length

    class ExperimentalSyntaxIncrementalDecoder(encodings.utf_8.IncrementalDecoder):
        def decode(self, input, final=False):
            self.buffer += input
            if final:
                buff = self.buffer
                self.buffer = b""
                text, _ = experimental_syntax_decode(buff)
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
            decode=experimental_syntax_decode,
            incrementalencoder=utf8.incrementalencoder,
            incrementaldecoder=ExperimentalSyntaxIncrementalDecoder,
            streamreader=encodings.utf_8.StreamReader,
            streamwriter=utf8.streamwriter,
        )

    codecs.register(search_function)
    console.configure(transform_source=transform_source)


register_encoding(
    encoding_name="experimental-syntax", transform_source=transform_source
)
