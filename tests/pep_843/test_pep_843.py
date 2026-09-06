from ideas.examples import pep_843
from ideas import remove_hook, current_state


def test_flat_layout():
    hook = pep_843.add_hook()

    from . import main_file

    assert main_file.__all__ == ['Widget', 'Gadget', 'cool', 'hot', 'a', 'b', 'c', 'd', 'spam', 'ham']
    remove_hook(hook)

# Currently, ideas cannot process modules with __init__.py files.
#
# def test_module_layout():
#     hook = pep_843.add_hook()
#     current_state.verbose = True

#     from .hub import __all__

#     assert __all__ == ['Widget', 'Gadget', 'cool', 'hot', 'a', 'b', 'c', 'd', 'spam', 'ham']

#     remove_hook(hook)


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


def test_star_import():
    source = "from a.b export *"
    expected_output = (
"""from a.b import *
__all__ = globals().setdefault("__all__", [])
__all__ = list(__all__)
import a.b
if hasattr(a.b, "__all__"):
    __all__.extend(list(a.b.__all__))
else:
    for _ in dir(a.b):
        if not _.startswith("_"):
            __all__.append(_)
""")
    assert pep_843.transform_source(source) == expected_output
