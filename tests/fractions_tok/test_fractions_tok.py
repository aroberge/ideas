from ideas.examples import fractions_tok
from ideas.import_hook import remove_hook


def test_simple_addition():
    hook = fractions_tok.add_hook()
    from . import addition  # noqa
    remove_hook(hook)
