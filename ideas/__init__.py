__version__ = "0.2.0"

from .session import current_state
from .import_hook import create_hook  # noqa


def remove_hook(hook):
    current_state.remove_hook(hook)


def disable_hook(hook):
    """Disable a given import hook. Use name="*" as a shortcut for
    disabling all hooks.

    Since many of the import hooks are found in the ideas.examples directory
    one can use "module_name" as an abbreviation of "ideas.examples.module_name".
    """
    current_state.disable_hook(hook)


def enable_hook(hook):
    """Enable a given import hook. Use name="*" as a shortcut for
    Enabling all hooks.

    Since many of the import hooks are found in the ideas.examples directory
    one can use "module_name" as an abbreviation of "ideas.examples.module_name".
    """
    current_state.enable_hook(hook)
