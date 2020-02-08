from ideas.examples import french
from ideas.import_hook import remove_hook


def test_french():
    hook = french.add_hook()

    try:
        import mon_programme  # for testing only this file
    except ImportError:
        from . import mon_programme  # for testing as part of a suite with pytest

    assert mon_programme.carré(4) == 16, "The square of 4 is 16"

    remove_hook(hook)


if __name__ == '__main__':
    test_french()
    print("Test completed succesfully")
