__version__ = "0.2.0"
import sys
import traceback

from .session import current_state
from .import_hook import create_hook


__all__ = [
    "add_patch",
    "create_hook",
    "current_state",
    "disable_hook",
    "enable_hook",
    "list_hooks",
    "remove_hook",
]

add_patch = current_state.add_patch
disable_hook = current_state.disable_hook
enable_hook = current_state.enable_hook
list_hooks = current_state.list_hooks
remove_hook = current_state.remove_hook


def exception_hook(exc_type, exc_value, tb):

    lines = traceback.format_exception_only(exc_value)

    if tb and exc_type.__name__ != "SyntaxError":
        traceback.print_tb(tb, limit=-1)
        print(f"{exc_type.__name__}: {exc_value}")
    else:
        for line in lines:
            print(line, end="")
        print()
    if not current_state.verbose:
        print("\nYou might want to use the command line flag --verbose or setting")
        print("session.current_state.verbose=True to get more details.")


sys.excepthook = exception_hook
