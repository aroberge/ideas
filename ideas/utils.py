"""utils.py
============

A few utility functions for this project.
"""

import os
import uuid

import token_utils  # to find the path of site-packages

PYTHON = os.path.dirname(os.__file__).lower()
SITE_PACKAGES = os.path.dirname(token_utils.__file__).lower()
IDEAS = os.path.dirname(__file__).lower()
TESTS = os.path.normpath(os.path.join(IDEAS, "..", "tests")).lower()
HOME = os.path.expanduser("~").lower()


def shorten_path(path):
    """Utility function used to reduce the length of the path shown
    to a user, including removing the extension.
    For example, a path for a module in the Python
    standard library might be shown as::

        PYTHON:/module

    whereas a file found in the user's root directory might be shown
    as::

         ~/file
    """
    # On Windows, the filenames are not case-sensitive
    # and the way Python displays filenames may vary.
    # To properly compare, we convert everything to lowercase
    # However, we ensure that the shortened path retains its cases
    ext = os.path.splitext(path)[1]

    path_lower = path.lower()
    path_lower = os.path.splitext(path_lower)[0]

    if path_lower.startswith(PYTHON):
        path = "PYTHON:" + path[len(PYTHON) : -len(ext)]
    elif path_lower.startswith(IDEAS):
        path = "IDEAS:" + path[len(IDEAS) : -len(ext)]
    elif path_lower.startswith(TESTS):
        path = "TESTS:" + path[len(TESTS) : -len(ext)]
    elif path_lower.startswith(SITE_PACKAGES):
        path = "SITE-PACKAGES:" + path[len(SITE_PACKAGES) : -len(ext)]
    elif path_lower.startswith(HOME):
        path = "~" + path[len(HOME) : -len(ext)]
    return path


def print_paths():
    """Prints the values of the path abbreviations used in shorten_path()."""
    print(f"~: {HOME}")
    print(f"PYTHON: {PYTHON}")
    print(f"IDEAS: {IDEAS}")
    print(f"SITE-PACKAGES {SITE_PACKAGES}")
    if os.path.exists(TESTS):
        print(f"TESTS: {TESTS}")


def print_source(source, header="Source"):
    """Prints a maximum of 10 lines of the source code.

    If there is a single line, it is prefixed by ``header: `.
    Otherwise, it is surrounded by dividers.

    ``header`` is usually either ``"Original"`` or ``"New"``
    """
    lines = source.split("\n")
    if len(lines) > 1:
        shortened_source_indicator = "\n..." if len(lines) > 10 else ""
        if len(lines) > 10:
            lines = lines[:10]
        while not lines[-1]:
            lines.pop()
        source = "\n".join(lines[:10]) + shortened_source_indicator
        print(f"\n#========== {header} ====")
        print(source)
        print(f"#=== End of {header} ====\n")
    else:
        print(f"{header}: {source}")


def generate_variable_names():
    """Generator that yields random variable names"""
    while True:
        name = uuid.uuid4()
        yield f"_{name.hex}"


def generate_predictable_names():
    """Generator that yields predictable variable names - useful for testing"""
    index = 0
    while True:
        index += 1
        yield f"_{index}"
