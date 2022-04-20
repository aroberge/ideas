
Ideas: making it easier to extend Python's syntax
========================================================

`Code on Github <https://github.com/aroberge/ideas>`_

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

This ... can be a rather daunting task. It might get a bit easier if
you grab a copy of the currently unpublished book by Anthony Shaw,
*CPython Internals* and read it from cover to cover,
but it will still remain a major task. Furthermore, it would not be easy
to share your work with others so that they can try it out.

However, **there is a simpler way:** it is possible to run code with a
modified syntax using import hooks [*or, in some cases as shown later,
using a custom codec*.]

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

**ideas** is designed to facilitate
the creation of such import hooks, and be a repository for
examples that can be used as starting points for new ideas.

Instead of figuring out how to write an import hook, using **ideas** you
can focus exclusively on what what might be needed to convert your proposed new
syntax into something that Python can understand -- **ideas** will
take care of the rest, including inserting it in ``sys.meta_path``.

.. warning::

    Doing something like what is described in this documentation
    is not recommended for production code.

    But it can be fun! ;-)


Quick links to topics
---------------------


.. toctree::
   :maxdepth: 1

    Additional motivation <motivation>
    Usage  <usage>
    Create your own import hook <function_keyword>
    A deep dive <possible>

    Guide to the examples <guide>

.. toctree::
   :maxdepth: 1
   :caption: Source transformations

    nobreak as a keyword <nobreak>
    repeat as a keyword <repeat>
    French Python <french>
    French repeat <french_repeat>
    Auto-self <auto_self>
    Decimal math <decimal_math>
    Fractional math (token) <fractional_math_tok>
    Switch statement <switch>
    Implicit multiplication <implicit_multiplication>
    Unnormalized unicode <unnormalized_unicode>

.. toctree::
   :maxdepth: 1
   :caption: AST transformations

    Fractional math (AST) <fractional_math_ast>

.. toctree::
   :maxdepth: 1
   :caption: Bytecode transformations

    Confused math (Bytecode) <bytecode>

.. toctree::
   :maxdepth: 1
   :caption: More complex examples

    True constants <constants>
    Examples never included - first draft <excluded>

.. toctree::
   :maxdepth: 1
   :caption: Custom encodings

    Create your own codec <lambda>

.. toctree::
   :maxdepth: 1
   :caption: Other modules

    About tokens <tokenize>
    <tokenize_notebook.ipynb>
    import_hook.py <import_hook>
    console.py <console>


To do
-----

.. todolist::


.. |tm| unicode:: U+000AE .. REGISTERED SIGN
