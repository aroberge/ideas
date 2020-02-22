Fractional math
==========================

.. admonition:: Summary

    - Demonstrates how to use an import hook that does an AST transformation
    - Demonstrates how to add code to initialize a module or the console
      with necessary imports and/or function definitions.


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


    >>> from ideas.examples import fractions_ast
    >>> hook = fractions_ast.add_hook()
    >>> from ideas import console
    >>> console.start()
    Configuration values for the console:
        source_init from source_init
        transform_ast from ideas.examples.fractions_ast
    --------------------------------------------------
    Ideas Console version 0.0.4. [Python version: 3.7.3]

    AST transformations applied: you will need to explicitly
    call print() to see the result of a command.

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

We can also achieve the same result using an import hook that
does a simple source transformation::

    >>> from ideas.examples import fractions_tok
    >>> hook = fractions_tok.add_hook()
    >>> from ideas import console
    >>> console.start()
    Configuration values for the console:
        source_init from source_init
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

The difference between the two is that, using the source transformation,
the REPL behaves as expected, printing out any unassigned result::

    ~>> # fractions_tok
    ~>> 1 / 10
    Fraction(1, 10)
    ~>>

However, this is not the case using the AST-based approach::

    ~>> # fractions_ast
    ~>> 1 / 10
    ~>>

In fact, even the underscore, `_`, does not have its usual meaning::

    ~>> # fractions_ast
    ~>> 1 / 10
    ~>> print(_)
    <ideas.import_hook.IdeasMetaFinder object at 0x02E42030>


.. automodule:: ideas.examples.fractions_ast
   :members:


.. automodule:: ideas.examples.fractions_tok
   :members:
