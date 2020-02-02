"""utils.py

A few useful objects which do not naturally fit anywhere else.
"""
import os.path


PYTHON = os.path.dirname(os.__file__).lower()
this_dir = os.path.dirname(__file__)
IDEAS = os.path.abspath(os.path.join(this_dir, "..")).lower()
TESTS = os.path.join(IDEAS, "tests").lower()
HOME = os.path.expanduser("~").lower()


def shorten_path(path):
    """Utility function used to reduce the length of the path shown
       to a user. For example, a path for a module in the Python
       standard library might be shown as::

           PYTHON:/module.py

       whereas a file found in the user's root directory might be shown
       as::

            ~/dir/file.py
    """
    # On windows, the filenames are not case sensitive
    # and the way Python displays filenames may vary.
    # To properly compare, we convert everything to lowercase
    # However, we ensure that the shortened path retains its cases
    path_lower = path.lower()
    current = os.getcwd()

    if path_lower.startswith(PYTHON):
        path = "PYTHON:" + path[len(PYTHON) :]
    elif path_lower.startswith(IDEAS):
        path = "IDEAS:" + path[len(IDEAS) :]
    elif path_lower.startswith(current):
        path = "CURRENT:" + path[len(current) :]
    elif path_lower.startswith(TESTS):
        path = "TESTS:" + path[len(TESTS) :]
    elif path_lower.startswith(HOME):
        path = "~" + path[len(HOME) :]
    return path


def print_paths():
    """Prints the values of the path abbreviations used in shorten_path()."""
    print(f"~: {HOME}")
    print(f"CURRENT: {os.getcwd()}")
    print(f"PYTHON: {PYTHON}")
    print(f"IDEAS: {IDEAS}")
    if os.path.exists(TESTS):
        print(f"TESTS: {TESTS}")
