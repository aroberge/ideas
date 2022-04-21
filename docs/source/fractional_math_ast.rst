.. admonition:: Summary

    - Demonstrates how to use an import hook that does an AST transformation

Fractional math (AST)
==========================


Consider the following standard Python code::

    >>> x = 1/10
    >>> for i in range(11):
    ...    print(i * x)
    ...
    0.0
    0.1
    0.2
    0.30000000000000004
    0.4
    0.5
    0.6000000000000001
    0.7000000000000001
    0.8
    0.9
    1.0

This is quite surprising for beginners, not familiar with the
limitations of representing floating point numbers.

However, we can "fix" this using an import hook that performs
and Abstract Syntax Tree (AST) transformation::

    > python -m ideas -a fractions_ast
       The following initializing code from ideas is included:

    from fractions import Fraction

    Ideas Console version 0.0.36. [Python version: 3.9.10]

    >>> x = 1/10
    >>> for i in range(11):
    ...    print(i * x)
    ...
    0
    1/10
    1/5
    3/10
    2/5
    1/2
    3/5
    7/10
    4/5
    9/10
    1
    >>> from ideas.session import config
    >>> config.show_changes = True
    >>> x = 1 / 10
    new: x = Fraction(1, 10)
    >>>


.. automodule:: ideas.examples.fractions_ast
   :members:
