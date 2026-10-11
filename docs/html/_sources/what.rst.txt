What is ideas?
===============

|ideas| is a package that makes it easier to write *import hooks*
used to **experiment** with alternative to Python's syntax.

What is an import hook?
-----------------------

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

|ideas| is designed to facilitate
the creation of such import hooks, and be a repository for
examples that can be used as starting points for new ideas.

Instead of figuring out how to write an import hook, using |ideas| you
can focus exclusively on what what might be needed to convert your proposed new
syntax into something that Python can understand: |ideas| will
take care of the rest for you.


Additional motivation for this project
--------------------------------------


While ideas such as the f-strings and **especially** the walrus operator
were discussed on Python-ideas and similar places, many people were
opposed to them being added to Python. This likely lead to the
following explanation added in `PEP 572 <https://www.python.org/dev/peps/pep-0572/#the-importance-of-real-code>`_:


    **The importance of real code**

    *During the development of this PEP many people (supporters and critics both) have had
    a tendency to focus on toy examples on the one hand, and on overly complex examples on the other.*

    *The danger of toy examples is twofold: they are often too abstract to make anyone go
    "ooh, that's compelling", and they are easily refuted with "I would never write it that way anyway".*

    *The danger of overly complex examples is that they provide a convenient strawman for critics
    of the proposal to shoot down ("that's obfuscated").*

    *Yet there is some use for both extremely simple and extremely complex examples: they are helpful
    to clarify the intended semantics.*

    -- `PEP 572 <https://www.python.org/dev/peps/pep-0572/#the-importance-of-real-code>`_


However, once it became possible for programmers to write their own code using
either the f-strings or the walrus operator instead of just reading
examples from PEP 572, it seems that
everyone became enthusiastic about them.

**If only it were possible to write short programs using currently invalid
syntax to truly get a feel for it rather than just complaining based
on reading a few examples.**  This is what |ideas| can help accomplish.

