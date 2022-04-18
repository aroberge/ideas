from ideas.examples import fractions_ast
from ideas.import_hook import remove_hook


def test_simple_addition():
    hook = fractions_ast.add_hook()
    from . import addition  # noqa
    remove_hook(hook)
