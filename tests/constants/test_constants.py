import sys
from ideas import _change_path_for_testing

NAME = "constants"
MODULE = None
HOOK = None
NB_HOOKS = len(sys.meta_path)  # Note: pytest adds its own hooks

# I want to be able to test this by itself, independent of pytest
# I cannot use the names "setup" and "teardown" otherwise pytest will raise
# an error


def set_up():
    global MODULE, HOOK
    _change_path_for_testing(NAME)
    MODULE = __import__(NAME)
    HOOK = MODULE.add_hook()


def tear_down():
    MODULE.remove_hook(HOOK)
    assert len(sys.meta_path) == NB_HOOKS, "Import hook properly removed"
    _change_path_for_testing(NAME, remove=True)


def test_uppercase():
    set_up()

    # The following module contains assertions confirming that it
    # is processed correctly when it is created.
    try:
        import uppercase
    except ImportError:
        from . import uppercase

    # The following confirm that attempts to modify it indirectly will fail
    assert uppercase.XX == 36, "Cannot change value of uppercase constant"
    del uppercase.XX
    uppercase.XX = "something else"
    assert uppercase.XX == 36, "Cannot change uppercase constant"

    # The following should not raise any error
    uppercase.new = 1
    uppercase.new = 3
    assert uppercase.new == 3, "Non constant values can be changed"
    del uppercase.new

    tear_down()


def test_final():
    set_up()

    # The following module contains assertions confirming that it
    # is processed correctly when it is created.
    try:
        import final
    except ImportError:
        from . import final

    # The following confirm that attempts to modify constants indirectly will fail
    assert final.const == 1, "In test: confirm initial value of final constant"
    final.const = 2
    final.const += 36
    assert final.const == 1, "In test: confirm value of final constant did not change"

    # The following should not raise any error
    final.new = 1
    final.new = 3
    assert final.new == 3, "Non constant values can be changed"
    del final.new

    tear_down()


if __name__ == "__main__":
    print("Testing uppercase:")
    test_uppercase()
    print("- " * 30)
    print("Testing final:")
    test_final()
    print("- " * 30)
    print("--> Success: test_constants.py ran as expected.")
