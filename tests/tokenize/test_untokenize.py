from ideas.utils import tokenize_source, untokenize

# Note: most of the tests involving untokenize have
# been adapted from https://github.com/myint/untokenize


def check(source, message):
    tokens = tokenize_source(source)
    new_source = untokenize(tokens)
    assert source == new_source, message


def test_untokenize():
    check(
        '''

def zap():

    """Hello zap.

  """; 1


    x \t= \t\t  \t 1


''',
        "From test_untokenize",
    )


def test_untokenize_with_tab_indentation():
    check(
        """
if True:
\tdef zap():
\t\tx \t= \t\t  \t 1
""",
        "From test_untokenize_with_tab_indentation",
    )


def test_untokenize_with_backslash_in_comment():
    check(r'''
def foo():
    """Hello foo."""
    def zap(): bar(1) # \
''', "From test_untokenize_with_backslash_in_comment")


def test_untokenize_with_escaped_newline():
    check(r'''def foo():
    """Hello foo."""
    x = \
            1
''', "From test_untokenize_with_escaped_newline")


def test_cpython_bug_35107():
    # Checking https://bugs.python.org/issue35107#msg328884
    check("#", "cpython bug - 1")
    check("#\n", "cpython bug - 2")
