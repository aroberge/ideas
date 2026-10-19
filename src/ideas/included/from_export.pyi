from _typeshed import Incomplete
from typing import Any

from ideas.ideas_hook import IdeasHook
import token_utils as tu

def insert_all_info(new_tokens: Incomplete, export_info: Incomplete) -> str: ...
def transform_source(
    source: str, filename: str | None = None, **_kwargs: dict[str, Any]
) -> str: ...
def add_hook(**_kwargs: Incomplete) -> IdeasHook: ...
