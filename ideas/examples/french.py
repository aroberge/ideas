"""French Python

Keywords are translated from French to English by a function in this file.

A "French Python" file is recognize by its pyfr extension.
"""
from ideas import import_hook, token_utils

# The name of the dict is irrelevant ... but we choose it to be the same
# as the file extension should be.
pyfr = {
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


def print_info(kind, source):
    """Prints the source code.

    ``kind`` is usually either ``"Original"`` or ``"Transformed"``
    """
    print(f"==========={kind}============")
    print(source)
    print("-----------------------------")


def transform_source(source, callback_params=None, **kwargs):
    """This function is called by the import hook loader and is used as a
    wrapper for the function where the real transformation is performed.
    """
    if callback_params is not None:
        if callback_params["show_original"]:
            print_info("Original", source)

    source = french_to_english(source)

    if callback_params is not None:
        if callback_params["show_transformed"]:
            print_info("Transformed", source)

    return source


def french_to_english(source):
    """A simple replacement of 'French Python keyword' by their normal
       English version.
    """
    new_tokens = []
    for token in token_utils.tokenize_source(source):
        if token.string in pyfr:
            token.string = pyfr[token.string]
        new_tokens.append(token)

    new_source = token_utils.untokenize(new_tokens)
    return new_source


def add_hook(show_original=False, show_transformed=False):
    """Creates and adds the import hook in sys.meta_path"""
    callback_params = {
        "show_original": show_original,
        "show_transformed": show_transformed,
    }
    hook = import_hook.create_hook(
        transform_source=transform_source,
        callback_params=callback_params,
        name=__name__,
        extensions=[".pyfr"],
    )
    return hook
