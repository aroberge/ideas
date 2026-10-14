from typing import Literal
from _typeshed import Incomplete

from ideas import create_hook, ideas_state
import token_utils

PREFIX: Incomplete
PREFIX_SHOWN: Literal[False] = False

def transform_source(
    source: Incomplete,
    callback_params: Incomplete = None,
    filename: Incomplete = None,
    module: Incomplete = None,
    **_kwargs: Incomplete,
) -> Incomplete: ...
def transform_units(source: Incomplete, prefix: Incomplete = "") -> Incomplete: ...
def add_hook(
    show_original: Incomplete = False,
    show_changes: Incomplete = False,
    **_kwargs: Incomplete,
) -> Incomplete: ...
