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

    assert module_a.const == 1, "In test: confirm initial value of final constant"
    module_a.const = 2
    module_a.const += 36
    assert module_a.const == 1, "In test: confirm value of final constant did not change"

    assert module_a.XX == 36, "Cannot change value of uppercase constant"
    del module_a.XX
    module_a.XX = "something else"
    assert module_a.XX == 36, "Cannot change uppercase constant"

    # The following should not raise any error
    module_a.new = 1
    module_a.new = 3
    assert module_a.new == 3, "Non constant values can be changed"
    del module_a.new

    enforce_constants.remove_hook(hook)
    assert len(sys.meta_path) == nb_hooks, "Import hook properly removed"

    _change_path_for_testing("enforce_constants", remove=True)


if __name__ == "__main__":
    test_enforce_constant_hook()
    print("- " * 30)
    print("Success: test_enforce_constants.py ran as expected.")
