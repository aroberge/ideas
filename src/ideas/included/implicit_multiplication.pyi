from typing import Any, Callable
from ideas.ideas_hook import IdeasHook

def transform_source(source: str, **_kwargs: dict[str, Any]) -> str: ...
def add_hook(
    transform_source: Callable[[str], str], **_kwargs: dict[str, Any]
) -> IdeasHook: ...
