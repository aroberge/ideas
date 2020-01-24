import os
import sys


current_dir = os.path.abspath(os.path.join(os.path.dirname(__file__)))
example_dir = os.path.abspath(
    os.path.join(current_dir, "..", "..", "examples", "enforce_constants")
)
if example_dir not in sys.path:
    sys.path.insert(0, example_dir)

nb_hooks = len(sys.meta_path)  # pytest adds its own hooks


def test_enforce_constant_hook():
    import enforce_constants

    hook = enforce_constants.add_hook()

    try:
        import module_a
    except ImportError:
        from . import module_a

    assert module_a.const == 1
    assert module_a.a_b == 4
    assert module_a.XX == 36
    assert module_a.YY == (1, 2, 4)

    # Attempt to change values from here

    module_a.const = 2
    module_a.const += 1
    module_a.XX = "something else"

    assert module_a.const == 1
    assert module_a.XX == 36

    enforce_constants.remove_hook(hook)
    assert len(sys.meta_path) == nb_hooks, "Import hook properly removed"


if __name__ == "__main__":
    test_enforce_constant_hook()
    print("test_enforce_constants.py ran as expected.")
