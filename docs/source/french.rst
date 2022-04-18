.. admonition:: Summary

    This example demonstrates the how to use a non-standard file
    extension (``.pyfr``) as an indication that an import hook must
    be used.

    It also demonstrates how to use the ``verbose_finder`` paramter.

French Python
==============

Imagine you are a French beginner who has learned the basics
of programming using a block-based environment such as Scratch
or Blockly. All the text shown on these blocks was in French,
the only language you know.  You now want to do a transition
to actually writing code in an editor, instead of putting
predefined blocks together. It would be so much easier if
you could use a version of Python where the keywords were in French,
with most of them being identical to what you were using in the
block-based environment.

This is what this import hook example allows one to do.
A more elaborate example is that given by
`AvantPy <https://aroberge.github.io/avantpy/docs/html/>`_.

Let's see it in action:

.. code-block:: none

   > python -m ideas -a french --show
   Ideas Console version 0.0.34. [Python version: 3.10.2]

   >>> pourchaque lettre dans 'Bonjour':
   ...    afficher(lettre)
   ...
   ===========Transformed============
   for lettre in 'Bonjour':
      print(lettre)

   -----------------------------
   B
   o
   n
   j
   o
   u
   r
   >>>

Importing .pyfr files
----------------------

Suppose we have the following two files:

.. code-block:: python

   # my_program.py

   print("Wrong one")
   raise ImportError

and

.. code-block:: none


   # my_program.pyfr

   afficher("Bonjour !")


Let's see if we attempt to import ``my_program`` after
setting up the ``french`` import hook::


   >>> from ideas.examples import french
   >>> hook = french.add_hook(verbose_finder=True)
   Looking for files with extensions:  ['.pyfr']
   The following paths will not be included in the search:
      PYTHON: c:\users\andre\appdata\local\programs\python\python310\lib
      IDEAS: c:\users\andre\github\ideas\ideas
      SITE-PACKAGES: c:\users\andre\github\ideas\venv-ideas3.10\lib\site-packages
   >>> import my_program
       Searching for ~\github\ideas\my_program.pyfr
       Found: ~\github\ideas\my_program.pyfr

   Bonjour !
   >>> import math
       Searching for ~\github\ideas\math.pyfr
       IdeasMetaFinder did not find math.pyfr

   >>> math.pi
   3.141592653589793
   >>>


API for french.py
--------------------

.. automodule:: ideas.examples.french
   :members:
