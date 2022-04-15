import pytest

from ideas.examples import repeat
from ideas.import_hook import remove_hook


def test_repeat():
    hook = repeat.add_hook()

    try:
        import my_program  # for testing only this file
    except ImportError:
        from . import my_program  # for testing as part of a suite with pytest
    assert my_program.one_loop == 4, "one_loop should equal 4"
    assert my_program.two_loops == 16, "two_loops should equal 16"

    remove_hook(hook)


def no_pytest_repeat_error():

    hook = repeat.add_hook()

    error_found = False
    try:
        import program_with_error
    except repeat.RepeatSyntaxError:
        error_found = True

    assert error_found, "RepeatSyntaxError was caught properly"
    remove_hook(hook)


def test_repeat_error():

    hook = repeat.add_hook()

    with pytest.raises(repeat.RepeatSyntaxError):
        from . import program_with_error

    remove_hook(hook)


source = """
repeat 3:
    repeat n * 22 : # comment
        pass
"""

converted = """
for _1 in range( 3):
    for _2 in range( n * 22 ): # comment
        pass
"""


def test_predictable():
    assert converted == repeat.transform_source(
        source, callback_params={'predictable_names':True}
    ), "Testing predicted conversion."


def test_predictable2():
    hook = repeat.add_hook(predictable_names=True)

    try:
        import my_program  # for testing only this file
    except ImportError:
        from . import my_program  # for testing as part of a suite with pytest
    assert my_program.one_loop == 4, "one_loop should equal 4"
    assert my_program.two_loops == 16, "two_loops should equal 16"

    remove_hook(hook)


def test_repeat_forever():
    source = "   repeat  forever:"
    assert repeat.transform_source(source) == "   while  True:", "repeat forever test"


def test_repeat_until():
    source = "repeat until condition: # a comment"
    assert repeat.transform_source(source) == "while not condition: # a comment"


def test_repeat_while():
    source = "repeat while condition:"
    # note extra space between while and condition as we removed a keyword
    assert repeat.transform_source(source) == "while  condition:"


if __name__ == "__main__":
    test_repeat()
    no_pytest_repeat_error()
    test_predictable()
    test_predictable2()
    test_repeat_forever()
    test_repeat_until()
    test_repeat_while()
    print("Tests completed.")
