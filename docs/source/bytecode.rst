Confused math
===============================

.. admonition:: Summary

    Demonstration of a simple bytecode transformation where
    we interchange ``BINARY_ADD`` and ``BINARY_MULTIPLY``.


Let's start with a demo from the console::

    >>> from ideas.examples import confused_math_bc
    >>> confused_math_bc.add_hook()
    <ideas.import_hook.IdeasMetaFinder object at 0x0317A590>
    >>> from ideas import console
    >>> console.start()
    Configuration values for the console:
        transform_bytecode from ideas.examples.confused_math_bc
    --------------------------------------------------
    Ideas Console version 0.0.4. [Python version: 3.7.3]

    ~>> x = 3
    ~>> x + x
    9
    ~>> x * x
    6

Yes, it is a silly example. However, I cannot come up with anything
possibly useful. Feel free to submit a better example.

.. automodule:: ideas.examples.confused_math_bc
   :members:
