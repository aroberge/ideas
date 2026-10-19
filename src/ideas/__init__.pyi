from typing import Callable

from ideas.session import ideas_state
from ideas.import_hook import create_hook
from ideas.ideas_hook import IdeasHook

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
add_patch: Callable[[str, Callable[..., None]], None]
disable_hook: Callable[[str | IdeasHook], None]
enable_hook: Callable[[str | IdeasHook], None]
list_hooks: Callable[[], None]
remove_hook: Callable[[str | IdeasHook], None]

def transform(source: str) -> None: ...
