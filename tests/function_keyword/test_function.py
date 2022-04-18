from ideas.examples import function_keyword
from ideas.import_hook import remove_hook


def test_function():
    hook = function_keyword.add_hook()
    from . import my_program
    assert my_program.square(4) == 16, "The square of 4 is 16"
    remove_hook(hook)
