from ideas.examples import fractions_ast
from ideas.import_hook import remove_hook


def test_simple_addition():
    hook = fractions_ast.add_hook()

    try:
        import addition  # for testing only this file
    except ImportError:
        from . import addition  # for testing as part of a suite with pytest
    remove_hook(hook)


if __name__ == "__main__":
    test_simple_addition()
    print("success")
