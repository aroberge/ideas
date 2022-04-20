"""
Keywords are translated from French to English/Python by a function in this file.

A "French Python" file is recognize by its .pyfr extension.
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
    """Creates and adds the import hook in sys.meta_path"""
    hook = import_hook.create_hook(
        transform_source=transform_source,
        hook_name=__name__,
        extensions=[".pyfr"],
    )
    return hook
