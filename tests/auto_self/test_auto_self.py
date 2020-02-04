from ideas.examples import auto_self
from ideas.import_hook import remove_hook


barebone_source = """
def __init__(self, *args):
    self .= :
        a
        b
        c
        d
    self.e = e
"""

barebone_expected = """
def __init__(self, *args):
    self.a = a
    self.b = b
    self.c = c
    self.d = d
    self.e = e
"""


def test_barebone():
    hook = auto_self.add_hook()

    assert auto_self.automatic_self(barebone_source) == barebone_expected, "Simple test"

    remove_hook(hook)


if __name__ == "__main__":
    test_barebone()
    print("Test completed successfully.")
