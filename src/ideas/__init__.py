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

add_patch = ideas_state.add_patch
disable_hook = ideas_state.disable_hook
enable_hook = ideas_state.enable_hook
list_hooks = ideas_state.list_hooks
remove_hook = ideas_state.remove_hook


def transform(source):
    """prints out the result of applying a source transformation on the argument."""
    print(ideas_state.source_transforms(source))
