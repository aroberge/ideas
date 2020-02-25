Fractional math (token)
==========================

.. admonition:: Summary

    - Demonstrates how to add code to initialize a module or the console
      with necessary imports and/or function definitions.

    `Source code <https://github.com/aroberge/ideas/blob/master/ideas/examples/fractions_tok.py>`_


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
integer into a ``Fraction`` instance::

    >>> from ideas.examples import fractions_tok
    >>> hook = fractions_tok.add_hook()
    >>> from ideas import console
    >>> console.start()
    Configuration values for the console:
        source_init from ideas.examples.fractions_tok
        transform_source from ideas.examples.fractions_tok
    --------------------------------------------------
    Ideas Console version 0.0.4. [Python version: 3.7.3]

    ~>> x = 1 / 10
    ~>> for i in range(11):
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

This example was created after a similar example using AST transformation
was created as a proof of concept. For more details about the
difference, please have a look at the AST-based example.

.. automodule:: ideas.examples.fractions_tok
   :members:
