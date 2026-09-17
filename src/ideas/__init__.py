from ideas.session import current_state
from ideas.import_hook import create_hook

__all__ = [
    "add_patch",
    "create_hook",
    "current_state",
    "disable_hook",
    "enable_hook",
    "list_hooks",
    "remove_hook",
    "transform",
]

add_patch = current_state.add_patch
disable_hook = current_state.disable_hook
enable_hook = current_state.enable_hook
list_hooks = current_state.list_hooks
remove_hook = current_state.remove_hook


def transform(source):
    """prints out the result of applying a source transformation on the argument."""
    print(current_state.source_transforms(source))
