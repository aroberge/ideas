What is ideas?
===============

.. |ideas| replace:: :small-caps-bold:`ideas`

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

.. sidebar:: A bit of a mess

    The code I wrote for the general ``import_hook.py`` code has grown "organically",
    adding or modifying features with almost every new examples. It works
    but is in great need of refactoring. Readers beware...

|ideas| is designed to facilitate
the creation of such import hooks, and be a repository for
examples that can be used as starting points for new ideas.

Instead of figuring out how to write an import hook, using |ideas| you
can focus exclusively on what what might be needed to convert your proposed new
syntax into something that Python can understand: |ideas| will
take care of the rest, including inserting it in ``sys.meta_path``.


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


.. tip::

    You can skip the rest of this section if you already know that you want to
    use an import hook and are not interested in the origin of this project.

Original motivation
-------------------

For more than 20 years, programming in Python has been my main hobby.
Other than for a few minor scripts, I did not use Python for my job.
However, for my hobby, I tried to focus on creating project to help Python learners
with `Reeborg's World <https://reeborg.ca>`_ and
`Friendly/friendly-traceback <https://friendly-traceback.github.io/docs/index.html>`_
being the best known ones.

As an amateur, I like to explore various ideas, learning along the way.
As I found myself doing a lot of copy-paste-modify on the various import
hooks experiments, including on some published projects such as the now
**deprecated/obsolete/abandoned**
`AvantPy <https://aroberge.github.io/avantpy/docs/html/>`_ 
as well as `various experiments I wrote about <https://duckduckgo.com/?q=experimental+site%3Aaroberge.blogspot.com>`_,
I thought it would make sense to create a versatile projects which I could
use as the basis of other projects.  An obvious benefit is that I now
need to fix bugs in a single project.  Furthermore, if this project gets
enough visibility, some programmers much more qualified than I am might
take the time to make concrete suggestions as to how to improve it.

Additional motivation
---------------------

Often, on the old Python-ideas mailing list,
and possibly on the `Python discuss ideas <https://discuss.python.org/c/ideas/6>`_` , 
a suggestion is made to someone that proposes something
new to try it by modifying Python using an import hook. For example:

    *You can pretty easily write an import hook to intercept module loading
    at the AST level and transform it however you want.*

        Andrew Barnert
        https://mail.python.org/pipermail/python-ideas/2015-May/033623.html

However, as Steve d'Aprano replied:

    *I think that the majority of Python programmers have no idea that you
    can even write an import hook at all, let alone how to do it.*

        https://mail.python.org/pipermail/python-ideas/2015-May/033633.html

I have yet to see a case of someone, other than perhaps some core developers,
following up on suggestions to try writing an import hook to test a
proposal on Python-ideas.
I believe, like Steve d'Aprano wrote, that the main reason is that most people
do not know how to do this.

So, by creating this project, I'm hoping that enough examples will
be created that could be **easily** adapted for exploring proposals
submitted to Python-ideas. If that is the case, I will likely benefit
as well as advanced Python programmers might be interested enough to
make suggestions as to how to improve this project.

About the name
--------------

For this project, I was thinking of using ``importhook`` (singular) or
``importhooks`` (plural). However, there was already a package named
``importhook`` on Pypi and I thought that using the plural form would
likely be just too confusing.

I settled on |ideas| as I am guessing that the main application would be
for people to try out suggestions from or for Python-ideas.

As I was looking at including other examples than the ones
I mentioned previously, I came accross Andrew Barnert's
`Stupid Python Ideas <http://stupidpythonideas.blogspot.com/>`_ blog,
which includes an older post about `Hacking Python with import hooks <http://stupidpythonideas.blogspot.com/2015/06/hacking-python-without-hacking-python.html>`_.
I have been thinking about adopting some of his examples, which I would not describe
as *stupid* but rather as *entertaining* ideas.
