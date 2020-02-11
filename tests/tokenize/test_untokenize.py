from ideas.token_utils import tokenize, untokenize

# Note: most of the tests involving untokenize have
# been adapted from https://github.com/myint/untokenize


def check(source):
    tokens = tokenize(source)
    new_source = untokenize(tokens)
    assert source == new_source


def test_untokenize():
    check(
        '''

def zap():

    """Hello zap.

  """; 1


    x \t= \t\t  \t 1


'''
    )


def test_untokenize_with_tab_indentation():
    check(
        """
if True:
\tdef zap():
\t\tx \t= \t\t  \t 1
"""
    )


def test_untokenize_with_backslash_in_comment():
    check(
        r'''
def foo():
    """Hello foo."""
    def zap(): bar(1) # \
'''
    )


def test_untokenize_with_escaped_newline():
    check(
        r'''def foo():
    """Hello foo."""
    x = \
            1
'''
    )


def test_cpython_bug_35107():
    # Checking https://bugs.python.org/issue35107#msg328884
    check("#")
    check("#\n")


def test_self():
    with open(__file__, "r") as f:
        source = f.read()
    check(source)
