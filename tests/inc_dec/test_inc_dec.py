from ideas.included import inc_dec


def test_simple_transformations():
    t = inc_dec.transform_source

    assert t("x++") == "(x, x := x + 1)[0]"
    assert t("x--") == "(x, x := x - 1)[0]"
    assert t("++x") == "(x, x := x + 1)[1]"
    assert t("--x") == "(x, x := x - 1)[1]"

    assert t("x--y") == "x--y"
    assert t("x---") == "x---"


def test_active_computation():
    inc_dec.add_hook()
    from . import source

    assert source.x == 3
