
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
modified syntax using import hooks.

    *I think that the majority of Python programmers have no idea that you
    can even write an import hook at all, let alone how to do it.*

        Steve d'Aprano
        https://mail.python.org/pipermail/python-ideas/2015-May/033633.html

That being said, not everyone might want to figure out how to write an import hook:

    | [page 420] *...it should be emphasized that Python's module, package and import
      mechanism is one of the most complicated parts of the entire language --
      often poorly understood by even the most seasoned Python programmers
      unless they've devoted effort to peeling back the covers.*
    |     ... long discussion ...
    | [page 428] *Assuming that your head hasn't completely exploded at this point, ...
      Last, but not least, spending some time sleeping with PEP 302 and the
      documentation for* importlib *under your pillow may be advisable.*

        Python Cookbook, 3rd edition, by David Beazley and Brian K. Jones


Another possibility
-------------------

In addition to using import hooks, it is possible to run code with a modified
syntax by using a specially crafted codec. See for example the `Pyxl project`_.
This is likely not as flexible as the approach we suggest using import hooks.

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

