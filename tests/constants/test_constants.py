from ideas.examples import constants
from ideas.import_hook import remove_hook


def test_uppercase():
    hook = constants.add_hook()

    # The following module contains assertions confirming that it
    # is processed correctly when it is created.

    from . import uppercase

    print("\nAttempting to change values of uppercase attributes.")
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

    remove_hook(hook)


def test_final(on_prevent_change=None):
    hook = constants.add_hook(on_prevent_change=on_prevent_change)

    # The following module contains assertions confirming that it
    # is processed correctly when it is created.

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

    remove_hook(hook)


def test_final_prevent_change():
    test_final(on_prevent_change=True)

