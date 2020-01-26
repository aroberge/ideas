Motivation for this project
============================

Original motivation
-------------------

Programming in Python is my main hobby.
As an amateur, I like to explore various ideas, learning along the way.
As I find myself doing a lot of copy-paste-modify on the various import
hooks experiments, including on some published projects such as
`AvantPy <https://aroberge.github.io/avantpy/docs/html/>`_,
I thought it would make sense to create a versatile projects which I could
use as the basis of other projects.  An obvious benefit is that I will
need to fix bugs in a single project.

Additional motivation
---------------------

Often, on python-ideas, a suggestion is made to someone that proposes something
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

    | [page 420] *...it should be emphasized that Python's module, package and import
      mechanism is one of the most complicated parts of the entire language --
      often poorly understood by even the most seasoned Python programmers
      unless they've devoted effort to peeling back the covers.*
    |     ... long discussion ...
    | [page 428] *Assuming that your head hasn't completely exploded at this point, ...
      Last, but not least, spending some time sleeping with PEP 302 and the
      documentation for* importlib *under your pillow may be advisable.*

        Python Cookbook, 3rd edition, by David Beazley and Brian K. Jones


So, by creating this project, I'm hoping that enough examples will
be created that could be **easily** adapted for exploring proposals
submitted to python-ideas. If that is the case, I will likely benefit
too as advanced Python programmers may make suggestions as to how
to improve this project.

About the name
--------------

For this project, I was thinking of using ``importhook`` (singular) or
``importhooks`` (plural). However, there is already a project named
``importhook`` on Pypi and I thought that using the plural form would
likely be just too confusing.

I settled on ``ideas`` as I am guessing that the main application would be
for people to try out suggestions from or for python-ideas.

