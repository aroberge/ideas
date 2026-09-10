"""This is a simple empty hook. Used as a default when only patching modules."""
from ideas import create_hook


def add_hook(**kwargs):
    return create_hook(name=__name__, first=True)
