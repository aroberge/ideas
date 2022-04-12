"""french_repeat.py
--------------------

Combining tranformations from two other examples.
"""

from ideas import import_hook, utils
from ideas.examples import french, repeat


additional_vocab = {
    "répéter": "repeat",
    "sansfin": "forever",
    "jusquà": "until",
}

french.fr_to_py.update(additional_vocab)


def transform_source(source, callback_params=None, **_kwargs):
    """This function is called by the import hook loader and uses
    transformations from two other examples.
    """
    if callback_params["show_original"]:
        utils.print_source(source, "Original")

    source = french.french_to_english(source)
    source = repeat.convert_repeat(source)

    if callback_params["show_transformed"]:
        utils.print_source(source, "Transformed")

    return source


def add_hook(
    show_original=False, show_transformed=False, verbose_finder=False, **_kwargs
):
    """Creates and adds the import hook in sys.meta_path"""
    callback_params = {
        "show_original": show_original,
        "show_transformed": show_transformed,
    }
    hook = import_hook.create_hook(
        transform_source=transform_source,
        callback_params=callback_params,
        hook_name=__name__,
        extensions=[".pyfr"],
        verbose_finder=verbose_finder,
    )
    return hook
