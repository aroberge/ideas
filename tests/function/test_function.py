from ideas.examples import function


def test_uppercase():
    hook = function.add_hook()

    try:
        import my_program  # for testing only this file
    except ImportError:
        from . import my_program  # for testing as part of a suite with pytest

    assert my_program.square(4) == 16, "The square of 4 is 16"

    function.tear_down(hook, my_program)


if __name__ == '__main__':
    test_uppercase()
