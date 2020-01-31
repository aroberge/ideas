Usage
=====

.. todo::

   Explain how to use the existing examples

.. todo::

   Brief explanation as to how to build your own import hook

Here's the content of a file where the programmer has indicated their
intent that the constant ``const`` should not change its value,
based on a type hint qualifier.

.. literalinclude:: ../../tests/constants/final.py

And here's what happens if we run an example.


    >>> from ideas.examples import function
    >>> hook = function.add_hook()
    >>> from ideas.console import start
    >>> start()
    ~>> sq = function x: x**2
    ~>> sq(3)
    9
