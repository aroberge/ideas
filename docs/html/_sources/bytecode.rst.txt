.. admonition:: Summary

   This example shows how to create an import hook that mutates a bytecode object.


Confused math
===============

This demonstrates what happens if we swap the meaning of
the ``BINARY_ADD`` and ``BINARY_MULTIPLY`` bytecodes.

.. code-block:: none

    > python -m ideas -a confused_math_bc
    Ideas Console version 0.0.34. [Python version: 3.10.2]
    
.. code-block::

    >>> x = 3
    >>> y = 7
    >>> x + y
    21
    >>> x * y
    10
    >>> # Python does simple mathematical operations *before*
    >>> # generating bytecode
    >>> z = 3 + 4
    >>> z
    7

Yes, it is a silly example. However, I cannot come up with anything
possibly useful to demonstrate the value of changing bytecode.
Feel free to submit a better example.

API for ``confused_math_bc``
----------------------------


.. automodule:: ideas.examples.confused_math_bc
   :members:
