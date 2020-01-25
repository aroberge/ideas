
Ideas: making it easier to extend Python's syntax
========================================================

To modify Python's syntax, normally all you need to do is:

1. Get a copy of the CPython's code repository and all the required compilers
   for your platform.
2. Modify the grammar file to add rules for the new syntax.
3. Modify the AST generation code; this requires a knowledge of C
4. Compile the AST into bytecode
5. Recompile the modified Python interpreter

However, there is a simpler way: it is possible to run code with a
modified syntax using import hooks. ``ideas`` is designed to facilitate
the creation of such import hooks, and be a repository for
examples that can be used as starting points for new ideas.


Quick links to topics
---------------------

.. toctree::
   :maxdepth: 1

    Motivation <motivation>
    Contents of various modules <modules>

.. toctree::
   :maxdepth: 1
   :caption: Examples

    True constants <constants>


To do
-----

.. todolist::


.. _Pyxl project: https://github.com/dropbox/pyxl

