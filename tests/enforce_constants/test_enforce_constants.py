import sys


# sys.dont_write_bytecode = True
nb_hooks = len(sys.meta_path)  # pytest adds its own hooks


def test_single_import():
    from ideas import enforce_constants  # noqa
    try:
        import module_a
    except ImportError:
        from . import module_a

    assert module_a.const == 1
    assert module_a.a_b == 4
    assert module_a.XX == 36
    assert module_a.YY == (1, 2, 4)

    del sys.meta_path[0]
    assert len(sys.meta_path) == nb_hooks, "Import hook properly removed"


if __name__ == '__main__':
    test_single_import()
    print("test_enforce_constants.py ran as expected.")
