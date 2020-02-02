
Ideas: making it easier to extend Python's syntax
========================================================

.. image:: _static/ideas.png
   :scale: 40 %
   :alt: ideas logo
   :align: center

You have an **Excellent Idea** |tm| to change the Python syntax and want
to find a way to include your
**Excellent Idea** |tm|  in your Python programs.
According to `Python Developers Guide <https://devguide.python.org/langchanges/>`_,
this might be doable if you are willing to follow "a few steps" including:

    1. Get a copy of the CPython's code repository and all the required compilers
       for your platform.
    2. Modify the grammar file to add rules for the new syntax.
    3. Modify the AST generation code; this requires a knowledge of C
    4. Compile the AST into bytecode
    5. Recompile the modified Python interpreter

This ... can be a rather daunting task.

But, there is a simpler way: it is possible to run code with a
modified syntax using import hooks.

What is an import hook
----------------------

.. sidebar:: Skipping over details.

    This is a simplified description. A more detailed explanation will
    be given later.

When you write something like::

    import my_module

Python's import machinery has to do the following:

    1. Try to use various tools to find the module requested
    2. Get the source code of that module
    3. Execute that source code, subject to some information reported in step 1.

An import hook is an additional tool that you create to do these three steps.
Once written, you add it to ``sys.meta_path`` so that Python's import
machinery can make use of it.


Still, writing import hooks can be rather difficult.


    | [page 420] *...it should be emphasized that Python's module, package and import
      mechanism is one of the most complicated parts of the entire language --
      often poorly understood by even the most seasoned Python programmers
      unless they've devoted effort to peeling back the covers.*
    |     ... long discussion ...
    | [page 428] *Assuming that your head hasn't completely exploded at this point, ...
      Last, but not least, spending some time sleeping with PEP 302 and the
      documentation for* importlib *under your pillow may be advisable.*

        **Python Cookbook, 3rd edition, by David Beazley and Brian K. Jones**

``ideas`` is designed to facilitate
the creation of such import hooks, and be a repository for
examples that can be used as starting points for new ideas.

Instead of figuring out how to write an import hook, using ``ideas`` you
can focus exclusively on what what might be needed to convert your proposed new
syntax into something that Python can understand -- ``ideas`` will
take care of the rest.

.. warning::

    Doing something like what is described in this documentation
    is not recommended for production code.

    But it can be fun! ;-)


Quick links to topics
---------------------

.. note::

    Most of the links below lead to mostly empty pages.
    Much more content will be added ... *soon*.


.. toctree::
   :maxdepth: 1

    Additional motivation -first draft <motivation>
    Usage - first draft <usage>
    Importing a module as main - todo <as_main>
    Overview of all possibilities - todo <possible>
    Examples never included - first draft<excluded>

.. toctree::
   :maxdepth: 1
   :caption: Examples

    function as a keyword - part 1 <function_simplest>
    function as a keyword - part 2 <function>
    nobreak as a keyword - todo <nobreak>
    French Python - todo <french>
    λ encoding - todo <lambda>
    repeat as a keyword - code implemented <repeat>
    Simple AST transformation - todo <ast>
    Simple bytecode transformation - todo <bytecode>
    Pythonic switch statement - todo  <switch>
    True constants - introduction done <constants>
    Json module - todo  <json>
    PEP 505: None-aware operators - todo  <pep_505>
    Import from non-standard locations - todo  <non_files>

.. toctree::
   :maxdepth: 1
   :caption: API

    import_hook.py <import_hook>
    utils.py <utils>
    console.py <console>



To do
-----

.. todolist::


.. |tm| unicode:: U+000AE .. REGISTERED SIGN
