"""
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

Let's see it in action:

.. code-block:: none

        > py -m ideas -a french --show
    Ideas Console version 0.2.0. [Python version: 3.11.9]
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

Suppose we have the following two files in the usage_demo folder:

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
verbose finder:

.. code-block:: none

    (venv-ideas3.11) C:\\Users\\Andre\\github\\ideas
    > py
    Python 3.11.9...
    >>> from ideas import current_state
    >>> current_state.verbose = True
    >>> from ideas.examples import french
    >>> french.add_hook()
    Added hook ideas.examples.french
    Looking for files with extensions:  ['.pyfr']
    The following paths will not be included in the search:
        PYTHON: c:\\users\\andre\\appdata\\local\\programs\\python\\python311\\lib
        SITE-PACKAGES: c:\\users\\andre\\github\\ideas\\venv-ideas3.11\\lib\\site-packages
        IDEAS: c:\\users\\andre\\github\\ideas\\ideas
    <Ideas import hook: ideas.examples.french>

    >>> from usage_demo import my_program
        Searching for ~\\github\\ideas\\usage_demo.pyfr
        IdeasMetaFinder did not find usage_demo.pyfr

        Searching for usage_demo.pyfr.pyfr
        IdeasMetaFinder did not find usage_demo.pyfr

        Searching for ~\\AppData\\Local\\Programs\\Python\\Python311\\python311.zip\\usage_demo.pyfr
        IdeasMetaFinder did not find usage_demo.pyfr

        Searching for ~\\AppData\\Local\\Programs\\Python\\Python311\\DLLs\\usage_demo.pyfr
        IdeasMetaFinder did not find usage_demo.pyfr

        Skipping over: PYTHON:
        Searching for ~\\AppData\\Local\\Programs\\Python\\Python311\\usage_demo.pyfr
        IdeasMetaFinder did not find usage_demo.pyfr

        Searching for ~\\github\\ideas\\venv-ideas3.11\\usage_demo.pyfr
        IdeasMetaFinder did not find usage_demo.pyfr

        Skipping over: SITE-PACKAGES:
        Searching for ~\\github\\ideas\\usage_demo\\my_program.pyfr
        Found: ~\\github\\ideas\\usage_demo\\my_program.pyfr

    Bonjour !
    >>> import math
    >>> math.pi
    3.141592653589793

.. caution::

    If you use two or more import hooks, only one of them will find your programs.
    If you have programs with different extensions, the order in which you add
    the import hooks may yield different results.

"""

from ideas import create_hook
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


def add_hook():
    """Creates and adds the import hook in sys.meta_path.
    Uses a custom extension for the exception hook."""
    hook = create_hook(
        transform_source=transform_source,
        name=__name__,
        extensions=[".pyfr"],
    )
    return hook
