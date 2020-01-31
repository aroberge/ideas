
Ideas: making it easier to extend Python's syntax
========================================================

.. image:: _static/ideas.png
   :scale: 40 %
   :alt: ideas logo
   :align: center

You have an **excellent** |tm| idea to change the Python syntax and want
to find a way to include your
**excellent** |tm| idea in your Python programs.
According to `Python Developers Guide <https://devguide.python.org/langchanges/>`_,
this might be doable if you are willing to follow "a few steps" including:

1. Get a copy of the CPython's code repository and all the required compilers
   for your platform.
2. Modify the grammar file to add rules for the new syntax.
3. Modify the AST generation code; this requires a knowledge of C
4. Compile the AST into bytecode
5. Recompile the modified Python interpreter

This ... is rather a daunting task.

However, there is a simpler way: it is possible to run code with a
modified syntax using import hooks. ``ideas`` is designed to facilitate
the creation of such import hooks, and be a repository for
examples that can be used as starting points for new ideas.

.. warning::

    Doing something like what is described in this documentation
    is not recommended for production code.

    But it can be fun! ;-)


Quick links to topics
---------------------

.. toctree::
   :maxdepth: 1

    Motivation <motivation>
    Usage <usage>
    Possibilities <possible>

.. toctree::
   :maxdepth: 1
   :caption: Examples

    True constants <constants>

.. toctree::
   :maxdepth: 1
   :caption: API

    import_hook.py <import_hook>
    utils.py <utils>



To do
-----

.. todolist::


.. _Pyxl project: https://github.com/dropbox/pyxl

.. |tm| unicode:: U+000AE .. REGISTERED SIGN
