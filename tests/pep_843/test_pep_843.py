from ideas.examples import pep_843


def test_ignore_from_inside_def():
    source = """
def test():
    from a export b
"""
    assert pep_843.transform_source(source) == source

    source = """
def test():
    from a export b

from c export d
"""
    expected_output = """
def test():
    from a export b

from c import d
__all__ = globals().setdefault("__all__", [])
__all__ = list(__all__)
__all__.extend(['d'])
"""
    assert pep_843.transform_source(source) == expected_output


def test_transform_single_line():
    source = "from module export name"
    expected_output =(
"""from module import name
__all__ = globals().setdefault("__all__", [])
__all__ = list(__all__)
__all__.extend(['name'])
""")
    assert pep_843.transform_source(source) == expected_output

    # Adding some indentation and other names
    source = "    from module export name, other_name as other"
    expected_output =(
"""    from module import name, other_name as other
    __all__ = globals().setdefault("__all__", [])
    __all__ = list(__all__)
    __all__.extend(['name', 'other'])
""")
    assert pep_843.transform_source(source) == expected_output

    source = "from module import name"
    assert pep_843.transform_source(source) == source

    source = "lazy from module export name"
    expected_output =(
"""lazy from module import name
__all__ = globals().setdefault("__all__", [])
__all__ = list(__all__)
__all__.extend(['name'])
""")
    assert pep_843.transform_source(source) == expected_output


def test_transform_two_lines():
    source = "from module export name\nfrom other_module export other_name"
    expected_output =(
"""from module import name
__all__ = globals().setdefault("__all__", [])
__all__ = list(__all__)
__all__.extend(['name'])
from other_module import other_name
__all__ = globals().setdefault("__all__", [])
__all__ = list(__all__)
__all__.extend(['other_name'])
""")
    assert pep_843.transform_source(source) == expected_output

    # Adding some indentation
    source = "    from module export name"
    expected_output =(
"""    from module import name
    __all__ = globals().setdefault("__all__", [])
    __all__ = list(__all__)
    __all__.extend(['name'])
""")
    assert pep_843.transform_source(source) == expected_output


def test_names_inside_parens():
    source = """
if True:
    from module export (a,  # pointless comment
    b,
c,
)
"""
    expected_output = """
if True:
    from module import (a,  # pointless comment
    b,
c,
)
    __all__ = globals().setdefault("__all__", [])
    __all__ = list(__all__)
    __all__.extend(['a', 'b', 'c'])
"""

    assert pep_843.transform_source(source) == expected_output