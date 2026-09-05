Usage
=====

.. important::

    As of August 18 2026, I've started updating this project after a 4 year hiatus. 
    The version that can be installed via pypi (using pip) has not been updated yet.

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


Using the ideas-enabled interactive console
---------------------------------------------

Ideas comes with its own interactive console.  Here's a sample session::


    >> from ideas.examples import function_keyword
    >>> function_keyword.add_hook()
    <Ideas import hook: ideas.examples.function_keyword>
    >>> from ideas import console
    >>> console.start()
    Ideas Console version 0.2.0. [Python version: 3.11.9]
    ideas> sq = function x: x*x
    ideas> sq(3)
    9


Just like with the normal CPython console, using the -i flag,
you can run a main script and continue with the interactive console::

    > python -im ideas -a function_keyword my_program
    16 is the square of 4.
    And the square of 5 is 25
    Ideas Console version 0.2.0. [Python version: 3.11.9]
    ideas> square(6)
    36


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
    <Ideas import hook: ideas.examples.function_keyword>
    >>> from ideas import console
    >>> console.start()
    Ideas Console version 0.2.0. [Python version: 3.11.9]
    ideas> sq = function x: x*x
    ideas> sq(3)
    9


Using with Pypy
-----------------

According to a few quick tests we did, **ideas** works with Pypy just
as well as it does with CPython.


Advanced usage
--------------

Information about more advanced usage can be found in this documentation.
You can also do the following in a terminal::

    python -m ideas -h

Multiple import hooks
---------------------

You can have multiple import hooks added; for example::

    (venv-ideas3.11) C:\Users\Andre\github\ideas
    > py -m ideas -a function_keyword -a nobreak
    Ideas Console version 0.2.0. [Python version: 3.11.9]
    ideas> import sys
    ideas> for finder in sys.meta_path:
    ...    print(finder)
    ...
    <IdeasMetaPathFinder for ideas.examples.nobreak>
    <IdeasMetaPathFinder for ideas.examples.function_keyword>
    <class '_frozen_importlib.BuiltinImporter'>
    <class '_frozen_importlib.FrozenImporter'>
    <class '_frozen_importlib_external.PathFinder'>

Note that once a meta_path finder finds the desired file to 
import, no other finder will be invoked. However, internally
**ideas** will do its best to combine all the required
transformations from all the ``IdeasHooks`` that will have
been activated.

Always running by default
-------------------------


.. danger::

    I do not recommend to install import hooks or codecs in you Python
    default installation.

If you **really** like to have your custom hook or custom encoding 
enabled by default, it is possible to do so, provided you
are not using a virtual environment. [2]_


.. sidebar::

    In the description below, setting ``PYTHONPATH`` in a terminal
    will only work as described
    if you install ideas in a normal (not virtual) environment.


In what follows, I will use the ``decimal_math`` example which
can be used either as an import hook or as a custom encoding.
`Source code <https://github.com/aroberge/ideas/blob/master/ideas/examples/decimal_math.py>`_

Import hook
~~~~~~~~~~~

To have decimal math working default, you can do the following.

1. Create a file named ``usercustomize.py`` containing the following:

.. code-block:: python

    from ideas.examples import decimal_math
    decimal_math.add_hook()

2. Assuming you are not in virtual environment, set the ``PYTHONPATH``
   environment variable to the path where ``usercustomize.py`` is found.
   On Windows, this is most done by navigating where this file is found
   and typing: ``set PYTHONPATH=%cd%``

You can now invoke your module doing the following::

    python -c "import my_script"


**I do not recommend that you do this.**

Custom codec
~~~~~~~~~~~~~

.. warning::

    Starting with Python 3.9, encodings cannot have an hyphen in their name
    such as::

        # coding: decimal-math

    Instead, they need to be normalized to using an underscore, as in::

        # coding: decimal_math

To have it useable by default as a custom codec, you can do the following.

1. Create a file named ``usercustomize.py`` containing the following:

.. code-block:: python

    from ideas.examples import decimal_math
    decimal_math.register()

2. Assuming you are not in virtual environment, set the ``PYTHONPATH``
   environment variable to the path where ``usercustomize.py`` is found.
   On Windows, this is most done by navigating where this file is found
   and typing: ``set PYTHONPATH=%cd%``

3. At the top of the module you wish to be run with the special codec,
   add the following two lines::

        # coding: decimal_math
        from decimal import Decimal

You can now invoke your module doing the following::

    python my_script.py

**Again, I do not recommend that you do this.**


.. raw:: html

    <hr>

.. [2] After not working on **ideas** for more than 4 years, I wanted to work on 
       the code again and make sure that everything was working correctly and couldn't figure 
       out why the ``usercustomize.py`` idea did not work. I deleted parts of the documentation
       where I had mentioned it until I remembered that it wouldn't work in a virtual
       environment.  Note that I didn't check that it **would** work in my main python 
       setup ... If it no longer works, please file an issue.