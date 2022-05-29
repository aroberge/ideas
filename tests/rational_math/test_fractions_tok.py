from ideas.examples import rational_math
from ideas.import_hook import remove_hook


def test_simple_addition():
    hook = rational_math.add_hook()
    from . import addition  # noqa
    remove_hook(hook)
