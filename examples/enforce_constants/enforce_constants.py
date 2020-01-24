import sys
from ideas import import_hook


def add_hook():
    hook = import_hook.create_hook()
    sys.meta_path.insert(0, hook)
    return hook


def remove_hook(hook):
    import_hook.remove_hook(hook)
