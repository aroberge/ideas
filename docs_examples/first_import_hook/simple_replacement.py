# simple_replacement.py
from ideas import import_hook


def some_arbitrary_name(source, **kwargs):
    return source.replace("function", "lambda")


import_hook.create_hook(transform_source=some_arbitrary_name, name=__name__)
