from typing import Callable
import codecs

utf8: codecs.CodecInfo | None

def register_encoding(
    encoding_name: str | None = None,
    transform_source: Callable[[str], str] | None = None,
    name: str | None = None,
) -> None: ...
