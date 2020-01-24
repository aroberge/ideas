import os
import sys

__version__ = "0.0.1"


def _change_path_for_testing(name, remove=False):

    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    example_dir = os.path.abspath(os.path.join(parent_dir, "examples", name))
    if remove:
        if example_dir in sys.path:
            sys.path.remove(example_dir)
    elif os.path.exists(example_dir) and example_dir not in sys.path:
        sys.path.insert(0, example_dir)
