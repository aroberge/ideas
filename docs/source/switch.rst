Pythonic switch statement
==========================

.. admonition:: Summary

    Adds a switch statement to Python.

    **Limitation**: a switch statement cannot contain another switch statement.

    `Source code <https://github.com/aroberge/ideas/blob/master/ideas/examples/switch.py>`_


There have been 2 PEPs looking at the possibility of adding a ``switch``
statement to Python.
First, in 2001, `PEP 275 <https://www.python.org/dev/peps/pep-0275/>`_ made
this suggestion. This was later superceded by `PEP 3103 <https://www.python.org/dev/peps/pep-3103>`_ written in 2006 by Guido van Rossum and, after a straw poll during
his keynote at PyCon 2007, he rejected it.

In order to "play" with the syntax and try to evaluate the benefit,
I decided to implement it. PEP 3103 looks at various possible syntax,
and I chose the one which seemed the most in line with normal Python syntax,
namely version 1 B. The implementation meant to replace code like::


    switch EXPR:
        case EXPR_1:
            SUITE
        case EXPR_2:
            SUITE
        case in (EXPR_3, EXPR_4, ...):
            SUITE
        ...
        else:
            SUITE

by::

    var_name = EXPR
    if var_name == EXPR_1:
            SUITE
    elif var_name == EXPR_2:
            SUITE
    elif var_name in (EXPR_3, EXPR_4, ...):
            SUITE
    else:
            SUITE
    del var_name


where ``var_name`` is a unique variable name chosen randomly.
Note that I didn't bother to dedent the inner ``SUITE`` as it is
never shown to the end user and would only complicate the code.

Result
------

The actual result is not particularly enlightning.
PEP 3103 considers the fact that each ``SUITE`` has two levels
of indentation to be a downside. Personally, after writing some testing
code with it (not saved anywhere), I found the fact that, due to having
all the ``case`` statements indented make the code stand out better than
having a traditional ``if/elif/else`` suite; so, I consider the extra
indentation to be a bonus. However, perhaps I might feel otherwise if I
always limited myself to having line with no more than 79 characters
which was the norm when the PEP was written.


.. automodule:: ideas.examples.switch
   :members:
