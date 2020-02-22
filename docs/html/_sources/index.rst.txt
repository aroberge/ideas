
Ideas: making it easier to extend Python's syntax
========================================================

`Code on Github <https://github.com/aroberge/ideas>`_

.. warning::

    If you see this warning, it is likely because you have stumbled upon
    this project prior to any public announcement.

    I am currently in the middle of writing this first draft for the
    documentation, occasionally changing the API of **Ideas**
    in an attempt to make it more user-friendly and adding/removing
    pages here. You cannot rely on any information written here ... yet.

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

``ideas`` is designed to facilitate
the creation of such import hooks, and be a repository for
examples that can be used as starting points for new ideas.

Instead of figuring out how to write an import hook, using ``ideas`` you
can focus exclusively on what what might be needed to convert your proposed new
syntax into something that Python can understand -- ``ideas`` will
take care of the rest, including inserting it in ``sys.meta_path``.

.. warning::

    Doing something like what is described in this documentation
    is not recommended for production code.

    But it can be fun! ;-)

Infrequently asked questions and comments
------------------------------------------

.. sidebar:: No FAQ

    In the absence of real questions having been asked,
    the following imaginary dialogue has been written before anyone else knew about
    this project.

**Why?**

Because it is fun. If this is not enough of a justification for you, have a look at
the motivation section which contains a longer, and possibly more serious answer.

**Is it safe to use in production code?**

No.

**But your example works perfectly well in my code; can I use it in my project?**

I don't think you should if your project is to be used by anyone else
but yourself.

**I found a bug.**

Wonderful, please file an issue so that I can perhaps fix it. Note however
that some examples are just proof of concepts and are not meant to be robust.

**Can I contribute code for a new example?**

Yes, please, by all means. But I suggest that you first create an issue that gives
an overview of what you wish to accomplish.

**I found a cool use of import hooks in another project, different from all of your examples.**

Please, give me the details and I will see if I can *easily* include
a similar example and if I think it is worthwhile to do so.

**I think that the explanation you have written for X could be improved upon.**

Please tell me more by filing an issue first and possibly creating a pull-request afterwards.

**I have an idea for a new example, but do not know how to write the code for it.**

First, make sure you go through all of the existing examples to confirm that
none can easily be adapted to do what you want.
If that is the case, file an issue ...
but please don't be offended if I don't write code for it
and end up closing the issue: I already have too many ideas of my own
for this project, too many other projects, and not
enough time to do all that I want.

**What about something like** ``from __future__ import braces`` **?**

No.

**In file X.py, you do not respect convention Y from PEP-8. This is unacceptable
in a Python project.**

*Seriously?*  This project is all about exploring potential changes
to Python's syntax, some of which are downright crazy, and you complain
about a PEP-8 violation? ...

Ok, perhaps you can tell me and it might make sense to change what I wrote.

**People from the Python-ideas mailing lists mentioned that I should look
at this project for my suggestion for a new syntax, but I don't know where to start.**

Just keep reading.


Quick links to topics
---------------------

.. sidebar:: Work in progress

    Most of the links below lead to mostly empty pages.
    Much more content will be added ... *soon*.


.. toctree::
   :maxdepth: 1

    Additional motivation <motivation>
    Usage  <usage>
    Create your own <function_simplest>
    A deep dive <possible>
    About tokens <tokenize>
    Tokenizing notebook <tokenize_notebook>

.. toctree::
   :maxdepth: 1
   :caption: Examples

    Improving function as a keyword <function>
    λ encoding and the main problem - to do <lambda>
    nobreak as a keyword - to do <nobreak>
    French Python - to do <french>
    Auto-self <auto_self>
    repeat as a keyword <repeat>
    Fractional math <ast>
    Simple bytecode transformation - todo <bytecode>
    Pythonic switch statement - to do  <switch>
    True constants <constants>
    Json module - todo  <json>
    Import from non-standard locations - to do  <non_files>
    Importing a module as main - to do <as_main>
    Examples never included - first draft<excluded>

.. toctree::
   :maxdepth: 1
   :caption: Other modules

    import_hook.py <import_hook>
    console.py <console>



To do
-----

.. todolist::


.. |tm| unicode:: U+000AE .. REGISTERED SIGN
