from ideas.examples import pep_843


def test_transform_single_line():
    source = "from module export name"
    expected_output =(
"""from module import name
__all__ = globals().setdefault("__all__", ['name'])
__all__.extend(['name'])
""")
    assert pep_843.transform_source(source) == expected_output

    # Adding some indentation
    source = "    from module export name"
    expected_output =(
"""    from module import name
    __all__ = globals().setdefault("__all__", ['name'])
    __all__.extend(['name'])
""")
    assert pep_843.transform_source(source) == expected_output


