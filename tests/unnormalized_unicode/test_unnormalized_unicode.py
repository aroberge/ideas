from ideas.examples import unnormalized_unicode
from ideas.import_hook import remove_hook


def test_unnormalized_unicode():
    hook = unnormalized_unicode.add_hook()
    from . import n_set  # noqa
    remove_hook(hook)