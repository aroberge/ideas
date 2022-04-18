from ideas.examples import confused_math_bc
from ideas.import_hook import remove_hook


def test_simple_case():
    hook = confused_math_bc.add_hook()
    from . import confused_math  # noqa
    remove_hook(hook)
