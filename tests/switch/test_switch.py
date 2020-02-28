from ideas.examples import switch
from ideas.import_hook import remove_hook


def test_transform():

    source = """
        switch EXPR:
            case EXPR_1:
                SUITE
            case EXPR_2:
                SUITE
            case in (EXPR_3, EXPR_4, ...):
                SUITE
            else:
                SUITE
        other_code"""

    expected = """
        _1 = EXPR
        if _1 == EXPR_1:
                SUITE
        elif _1 == EXPR_2:
                SUITE
        elif _1 in (EXPR_3, EXPR_4, ...):
                SUITE
        else:
                SUITE
        del _1
        other_code"""

    result = switch.convert_switch(source, predictable_names=True)
    assert result == expected, "Switch conversion test"


def test_switch1():
    hook = switch.add_hook()

    try:
        import switch1  # for testing only this file
    except ImportError:
        from . import switch1  # for testing as part of a suite with pytest

    remove_hook(hook)


if __name__ == '__main__':
    test_transform()
    test_switch1()
    print("Done.")
