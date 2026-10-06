from ideas.included import nobreak


def test_for():
    source_for = """for i in range(10):
    pass
%s:
    pass"""

    source = source_for % "nobreak"
    result = nobreak.transform_source(source)
    expected = source_for % "else"

    assert result == expected, "nobreak with for"


def test_while():
    source_while = """while True:
    pass
%s:
    pass"""

    source = source_while % "nobreak"
    result = nobreak.transform_source(source)
    expected = source_while % "else"

    assert result == expected, "nobreak with while"


def test_from_file():
    import os

    current_dir = os.getcwd()
    this_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(this_dir)
    with open("nobreak_in.txt", "r") as f:
        source = f.read()

    with open("nobreak_out.txt", "r") as f:
        expected = f.read()

    result = nobreak.transform_source(source)
    assert result == expected, "nobreak from file"
    os.chdir(current_dir)
