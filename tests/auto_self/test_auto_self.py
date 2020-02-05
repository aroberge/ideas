from ideas.examples import auto_self
from ideas.import_hook import remove_hook


cls_source = """
def __init__(cls, *args, **kwargs):
    cls .= :
        a
        b
        x
        y
        c = [] if __ is None else __
        d
        f = 0 if __ < 0 else __
    cls.e = e
"""

cls_expected = """
def __init__(cls, *args, **kwargs):
    cls.a = a
    cls.b = b
    cls.x = x
    cls.y = y
    cls.c = [] if c is None else c
    cls.d = d
    cls.f = 0 if f < 0 else f
    cls.e = e
"""

pep_557_expected = """
class Application:
    def __init__(
        self,
        name,
        requirements,
        constraints=None,
        path="",
        executable_links=None,
        executables_dir=(),
    ):
        self.name = name
        self.requirements = requirements
        self.constraints = {} if constraints is None else constraints
        self.path = path
        self.executable_links = [] if executable_links is None else executable_links
        self.executables_dir = executables_dir

        self.additional_items = []
"""

pep_557_source = """
class Application:
    def __init__(
        self,
        name,
        requirements,
        constraints=None,
        path="",
        executable_links=None,
        executables_dir=(),
    ):
        self .= :
            name
            requirements
            constraints = {} if __ is None else __
            path
            executable_links = [] if __ is None else __
            executables_dir

        self.additional_items = []
"""

pep_557_source_other = """
class Application:
    def __init__(
        cls,
        name,
        requirements,
        constraints=None,
        path="",
        executable_links=None,
        executables_dir=(),
    ):
        cls .= :
            name
            requirements
            constraints = {} if constraints is None else __
            path
            executable_links = [] if __ is None else executable_links
            executables_dir

            additional_items = []
"""


def test_barebone():
    hook = auto_self.add_hook()
    result = auto_self.automatic_self(cls_source)

    assert result == cls_expected, "auto_self test"

    remove_hook(hook)


def test_pep_557():
    hook = auto_self.add_hook()
    result = auto_self.automatic_self(pep_557_source)

    assert result == pep_557_expected, "PEP 557 auto_self test"

    result_other = auto_self.automatic_self(pep_557_source_other)
    result_other = result_other.replace("cls", "self")

    assert result_other == pep_557_expected, "PEP 557 auto_self test other"

    remove_hook(hook)


if __name__ == "__main__":
    test_barebone()
    print("Test completed successfully.")
