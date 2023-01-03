from ideas.examples import polish_expr
from ideas.import_hook import remove_hook


def test_polish_expr():
    hook = polish_expr.add_hook()
    from . import polish  # noqa
    remove_hook(hook)
    assert polish.x == 11
    assert polish.y == 110
    assert polish.z == 505
