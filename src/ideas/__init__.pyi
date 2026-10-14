from typing import Callable
from _typeshed import Incomplete

from ideas.session import ideas_state
from ideas.import_hook import create_hook

__all__ = [
    "add_patch",
    "create_hook",
    "ideas_state",
    "disable_hook",
    "enable_hook",
    "list_hooks",
    "remove_hook",
    "transform",
]
add_patch: Callable[[Incomplete, Incomplete], Incomplete]
disable_hook: Callable[[Incomplete], Incomplete]
enable_hook: Callable[[Incomplete], Incomplete]
list_hooks: Callable[[], Incomplete]
remove_hook: Callable[[Incomplete], Incomplete]

def transform(source: str) -> None: ...
