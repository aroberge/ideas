"""utils.py
============

A few utility functions for this project.
"""

import os
import uuid

PYTHON = os.path.dirname(os.__file__).lower()
IDEAS = os.path.dirname(__file__).lower()
TESTS = os.path.normpath(os.path.join(IDEAS, "..", "tests")).lower()
HOME = os.path.expanduser("~").lower()


def shorten_path(path):
    """Utility function used to reduce the length of the path shown
       to a user. For example, a path for a module in the Python
       standard library might be shown as::

           PYTHON:/module.py

       whereas a file found in the user's root directory might be shown
       as::

            ~/file.py
    """
    # On windows, the filenames are not case sensitive
    # and the way Python displays filenames may vary.
    # To properly compare, we convert everything to lowercase
    # However, we ensure that the shortened path retains its cases
    path_lower = path.lower()

    if path_lower.startswith(PYTHON):
        path = "PYTHON:" + path[len(PYTHON) :]
    elif path_lower.startswith(IDEAS):
        path = "IDEAS:" + path[len(IDEAS) :]
    elif path_lower.startswith(TESTS):
        path = "TESTS:" + path[len(TESTS) :]
    elif path_lower.startswith(HOME):
        path = "~" + path[len(HOME) :]
    return path


def print_paths():
    """Prints the values of the path abbreviations used in shorten_path()."""
    print(f"~: {HOME}")
    print(f"PYTHON: {PYTHON}")
    print(f"IDEAS: {IDEAS}")
    if os.path.exists(TESTS):
        print(f"TESTS: {TESTS}")


def print_source(source, header="Source"):
    """Prints the source code.

    ``header`` is usually either ``"Original"`` or ``"Transformed"``
    """
    print(f"==========={header}============")
    print(source)
    print("-----------------------------")


def generate_variable_names():
    """Generator that yields random variable names"""
    while True:
        name = uuid.uuid4()
        yield "_%s" % name.hex


def generate_predictable_names():
    """Generator that yields predictable variable names - useful for testing"""
    n = 0
    while True:
        n += 1
        yield "_%s" % n
