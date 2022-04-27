"""
.. admonition:: Summary

    This example demonstrates the how to use a non-standard file
    extension (``.pyfr``) as an indication that an import hook must
    be used.

    It also demonstrates how to use the ``verbose_finder`` configuration option.

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
    Ideas Console version 0.0.38. [Python version: 3.9.10]

    ideas> pourchaque lettre dans 'Bonjour':
       ...     afficher(lettre)
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

    ideas>


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
setting up the ``french`` import hook and enabling the
verbose finder::


   >>> from ideas.session import config
   >>> config.verbose_finder = True
   >>> from ideas.examples import french
   >>> hook = french.add_hook()
   Looking for files with extensions:  ['.pyfr']
   The following paths will not be included in the search:
      PYTHON: c:\\users\\andre\\appdata\\local\\programs\\python\\python37\\lib
      IDEAS: c:\\users\\andre\\github\\ideas\\ideas
      SITE-PACKAGES: c:\\users\\andre\\github\\ideas\\venv-ideas3.7\\lib\\site-packages
   >>> import my_program
       Searching for ~\\github\\ideas\\my_program.pyfr
       Found: ~\\github\\ideas\\my_program.pyfr

   Bonjour !
   >>> import math
       Searching for ~\\github\\ideas\\math.pyfr
       IdeasMetaFinder did not find math.pyfr

   >>> math.pi
   3.141592653589793
   >>>
"""
from ideas import import_hook
import token_utils

fr_to_py = {
    "Faux": "False",
    "Aucun": "None",
    "Vrai": "True",
    "et": "and",
    "comme": "as",
    "affirmer": "assert",
    "async": "async",  # do not translate
    "await": "await",  # as these are not for beginners
    "interrompre": "break",
    "classe": "class",
    "continuer": "continue",
    "définir": "def",
    "supprimer": "del",
    "sinonsi": "elif",
    "sinon": "else",
    "siexception": "except",
    "finalement": "finally",
    "pourchaque": "for",
    "de": "from",
    "global": "global",
    "si": "if",
    "importer": "import",
    "dans": "in",
    "est": "is",
    "fonction": "lambda",
    "nonlocal": "nonlocal",
    "pas": "not",
    "ou": "or",
    "passer": "pass",
    "lever": "raise",
    "retourner": "return",
    "essayer": "try",
    "tantque": "while",
    "avec": "with",
    "céder": "yield",
    # a few builtins useful for beginners
    "demander": "input",
    "afficher": "print",
    "intervalle": "range",
    "quitter": "exit",  # useful for console
}


def transform_source(source, **_kwargs):
    """A simple replacement of 'French Python keyword' by their normal
    English version.
    """
    new_tokens = []
    for token in token_utils.tokenize(source):
        if token.string in fr_to_py:
            token.string = fr_to_py[token.string]
        new_tokens.append(token)

    new_source = token_utils.untokenize(new_tokens)
    return new_source


def add_hook(**_kwargs):
    """Creates and adds the import hook in sys.meta_path.
    Uses a custom extension for the exception hook."""
    hook = import_hook.create_hook(
        transform_source=transform_source,
        hook_name=__name__,
        extensions=[".pyfr"],
    )
    return hook
