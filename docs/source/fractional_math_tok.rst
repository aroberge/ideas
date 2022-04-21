.. admonition:: Summary

   This is another example of a source transformation.
   In a later section, we will do essentially the same but using an
   Abstract Syntax Tree (AST) transformation, which is a more robust
   approach for this type of example.

Fractional math (token)
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

However, we can "fix" this using an import hook that wraps
integer, which are followed by a ``/``, into a ``Fraction`` instance::

    > python -m ideas -a fractions_tok
       The following initializing code from ideas is included:

    from fractions import Fraction

    Ideas Console version 0.0.36. [Python version: 3.7.9]

    >>> x =  1 / 10
    >>> for i in range(11):
    ...     print(i * x)
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
    new: x = Fraction(1) / 10
    >>>

This example was created after a similar example using AST transformation
was created as a proof of concept. For more details about the
difference, please have a look at the AST-based example.

.. automodule:: ideas.examples.fractions_tok
   :members:
