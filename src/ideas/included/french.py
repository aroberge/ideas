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

    Python 3.11.9 <...>
    >>> from ideas import ideas_state
    >>> ideas_state.verbose_finder = True
    >>> ideas_state.verbose = True
    >>> from ideas.included import french
    >>> french.add_hook()
    Added hook ideas.included.french
    Looking for files with extensions:  ['.pyfr']
    The following paths will not be included in the search:
    ~/AppData/Local/Programs/Python/Python311/Lib C:\Users\Andre\AppData\Local\Programs\Python\Python311\Lib
    ~/github/token-utils/src/token_utils C:\Users\Andre\github\token-utils\src\token_utils
    src/ideas C:\Users\Andre\github\ideas\src\ideas
    <Ideas import hook: ideas.included.french>
    >>> import mon_programme

    ideas.included.french.find_spec():
    No search paths were specified.
    Will use the current directory as well as paths included in sys.path
    These are the potential search paths
        docs_examples/french

        ~/AppData/Local/Programs/Python/Python311/python311.zip
        ~/AppData/Local/Programs/Python/Python311/DLLs
        ~/AppData/Local/Programs/Python/Python311/Lib
        ~/AppData/Local/Programs/Python/Python311
        ~/github/common_venv
        ~/github/common_venv/Lib/site-packages
        src
        ~/github/token-utils/src

    The following have been set as 'excluded' for this import hook.
        ~/AppData/Local/Programs/Python/Python311/Lib
        ~/github/token-utils/src/token_utils
        src/ideas

    These are the remaining search paths:
        docs_examples/french

        ~/AppData/Local/Programs/Python/Python311/python311.zip
        ~/AppData/Local/Programs/Python/Python311/DLLs
        ~/AppData/Local/Programs/Python/Python311
        ~/github/common_venv
        ~/github/common_venv/Lib/site-packages
        src
        ~/github/token-utils/src
    FOUND 'C:\Users\Andre\github\ideas\docs_examples\french\mon_programme.pyfr'

    ideas.included.french.find_spec():
    <IdeasMetaPathFinder for ideas.included.french> cannot find 'unicodedata'
    >>> carré(4)
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    NameError: name 'carré' is not defined

    >>> mon_programme.carré(4)
    16

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


def add_hook(**_kwargs):
    """Creates and adds the import hook in sys.meta_path.
    Uses a custom extension for the exception hook."""
    hook = create_hook(
        transform_source=transform_source,
        name=__name__,
        extensions=[".pyfr"],
    )
    return hook
