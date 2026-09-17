import sys
import traceback

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


def exception_hook(exc_type, exc_value, tb):
    """Custom exception hook. Set current_state.verbose=True
    if you wish to use Python's standard exception hook.
    """

    if current_state.verbose:
        sys.__excepthook__(exc_type, exc_value, tb)
        return

    if tb and exc_type.__name__ != "SyntaxError":
        traceback.print_tb(tb, limit=-1)
        print(f"{exc_type.__name__}: {exc_value}")
    else:
        error_string = "".join(
            traceback.format_exception(
                type(exc_value), exc_value, exc_value.__traceback__
            )
        )
        print(error_string)


sys.excepthook = exception_hook
