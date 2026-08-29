from ideas.examples import french
from ideas import remove_hook


def test_french():
    hook = french.add_hook()
    from . import mon_programme
    assert mon_programme.carré(4) == 16, "The square of 4 is 16"  # noqa
    remove_hook(hook)
