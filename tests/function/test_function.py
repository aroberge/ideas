from ideas.examples import function, function_simplest
from ideas.import_hook import remove_hook


def test_function():
    hook = function.add_hook()

    try:
        import my_program  # for testing only this file
    except ImportError:
        from . import my_program  # for testing as part of a suite with pytest
    assert my_program.square(4) == 16, "The square of 4 is 16"

    remove_hook(hook)


def test_function_simplest():
    hook = function_simplest.add_hook()

    try:
        import my_program
    except ImportError:
        from . import my_program
    assert my_program.square(-3) == 9, "The square of -3 is 9"

    remove_hook(hook)


if __name__ == '__main__':
    test_function()
    test_function_simplest()
