"""french_repeat.py
--------------------

Combining transformations from two other examples.
"""

from ideas import import_hook
from ideas.examples import french, repeat


additional_vocab = {
    "répéter": "repeat",
    "sansfin": "forever",
    "jusquà": "until",
}

french.fr_to_py.update(additional_vocab)


def transform_source(source, **_kwargs):
    """This function is called by the import hook loader and uses
    transformations from two other examples.
    """
    source = french.transform_source(source)
    source = repeat.transform_source(source)
    return source


def add_hook(**_kwargs):
    """Creates and adds the import hook in sys.meta_path"""
    hook = import_hook.create_hook(
        transform_source=transform_source,
        hook_name=__name__,
        extensions=[".pyfr"],
    )
    return hook
