Usage
=====

.. admonition:: Hello World!

    All the examples below, as well as a few other mentioned later,
    are based on an import hook which makes
    it possible to use the word ``function`` as being equivalent
    to the Python keyword ``lambda``.

    Think of this simple example as the ``"Hello World!"`` for this project.


Basic usage
-----------

Suppose that you want to use ``function`` as a keyword in Python, to mean
the same thing as ``lambda``, enabling you to write::

    # my_program.py

    square = function x: x**2
    print(f"{square(4)} is the square of 4.")

    if __name__ == '__main__':
        print(f"And the square of 5 is {square(5)}")


You can run this program in a terminal as follows::

    > python -m ideas my_program -a function_keyword
    16 is the square of 4.
    And the square of 5 is 25


The argument following ``-a`` is the name of a module that contains
a function named ``add_hook``.  A search for such a module is first
done in the current directory. If the module is not found in the
current directory, it is assumed to exists in the ``ideas.examples``
directory included with **ideas**.

You may have noticed in the above that ``my_program`` does not
include a ``.py`` extension. This is because ``my_program`` is imported:
Python **import hooks**, by definition, only work on modules that are
imported. Yet, you may have also noticed that it is imported with
the name ``'__main__'``, so that it is run as though it is the main script.

.. sidebar:: .py extension?

    Ideas is quite forgiving. If you invoke it adding a ``.py`` extension
    to the main script, as in:

    .. code-block:: none

        > python -m ideas my_program.py -a function_keyword

    it will work the same way as if you left out the ``.py`` extension.


Using the ideas-enabled interactive console
---------------------------------------------

Ideas comes with its own interactive console.  Here's a sample session::


    > python -m ideas -a function_keyword
    Ideas Console version 0.0.31. [Python version: 3.10.2]

    >>> cube = function x: x**3
    >>> cube(3)
    27


Just like with the normal CPython console, using the -i flag,
you can run a main script and continue with the interactive console::

    > python -im ideas my_program.py -a function_keyword
    16 is the square of 4.
    And the square of 5 is 25
    Ideas Console version 0.0.31. [Python version: 3.10.2]

    >>> square(6)
    36
    >>> cube = function x: x**3
    >>> cube(6)
    216


Using with IPython or Jupyter notebook/lab
-------------------------------------------

You can also use it with IPython, either in a terminal or in a Jupyter environment.
Here is an example using IPython in a terminal.


.. code-block:: ipython

    In [1]: from ideas.examples import function_keyword

    In [2]: function_keyword.add_hook()
    Out[2]: <IdeasMetaFinder object for ideas.examples.function_keyword>

    In [3]: cube = function x: x** 3

    In [4]: cube(3)
    Out[4]: 27

Starting from a standard CPython interpreter
----------------------------------------------

Unlike the IPython interactive interpreter (aka 'shell'), the CPython
interpreter does not support directly transformations done by ideas.
It is however possible to start the ideas console from the CPython
interactive interpreter.

.. code-block:: python

    >>> from ideas.examples import function_keyword
    >>> function_keyword.add_hook()
    <IdeasMetaFinder object for ideas.examples.function_keyword>
    >>> from ideas import console
    >>> console.start()
    Ideas Console version 0.0.34. [Python version: 3.10.2]

    ~>> sq = function x: x**2
    ~>> sq(3)
    9

In this case, the ideas prompt ``~>>`` is different from the CPython one.


Using with Pypy
-----------------

According to a few quick tests we did, **ideas** works with Pypy just
as well as it does with CPython.


Advanced usage
--------------

Information about more advanced usage can be found in this documentation.
You can also do the following in a terminal::

    python -m ideas -h
