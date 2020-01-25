import sys


nb_hooks = len(sys.meta_path)  # pytest adds its own hooks


def test_enforce_constant_hook():
    from ideas import _change_path_for_testing
    _change_path_for_testing("enforce_constants")

    import enforce_constants
    hook = enforce_constants.add_hook()

    try:
        import module_a
    except ImportError:
        from . import module_a

    # Inside our test modules, we had constants defined, which we
    # attempted to reassign.
    # We confirm that the initial value was not changed.

    assert module_a.const == 1, "Cannot change value of final constant"
    assert module_a.XX == 36, "Cannot change value of uppercase constant"
    assert module_a.YY == (1, 2, 4), "Cannot change value of uppercase tuple constant"

    # Next, we show that we cannot change the values of the constants
    # by attempting to change their attribute.

    module_a.const = 2
    # module_a.const += 1, "Cannot do indirect augmented assignment"
    module_a.XX = "something else"

    assert module_a.const == 1, "Cannot indirectly change value of final constant"
    assert module_a.XX == 36, "Cannot change value of uppercase constant"

    del module_a.XX
    assert module_a.XX == 36, "Cannot delete constant from module"

    # The following should not raise any error
    module_a.new = 1
    module_a.new = 3
    del module_a.new

    enforce_constants.remove_hook(hook)
    assert len(sys.meta_path) == nb_hooks, "Import hook properly removed"

    _change_path_for_testing("enforce_constants", remove=True)


if __name__ == "__main__":
    test_enforce_constant_hook()
    print("test_enforce_constants.py ran as expected.")
