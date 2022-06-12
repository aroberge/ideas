"""This module defines a utility for patching modules.

It is based on the recipe found in section 10.12 of the third
edition of the Python Cookbook."""

import importlib
import sys
from collections import defaultdict

PATCHES = defaultdict(list)


class PatchingFinder:
    def __init__(self):
        self.found_once = set()

    def find_module(self, fullname, path=None):
        if fullname in self.found_once:
            return None

        self.found_once.add(fullname)
        return PatchingLoader(self)


sys.meta_path.insert(0, PatchingFinder())


class PatchingLoader:
    def __init__(self, finder):
        self._finder = finder

    def load_module(self, fullname):
        """Loads a module and potentially apply patches"""
        # Use the normal importing machinery. This time, PatchingFinder
        # will skip over the module as it will already been found.
        importlib.import_module(fullname)
        module = sys.modules[fullname]
        for patch in PATCHES[fullname]:
            module = patch(module)
        return module


def add_patch(module_name, func):
    """Adds patch to be applied to a module.

    ``module_name``: the full name of the module to be patched
    ``func``: a callable which takes as a single argument a module object
    and returns a modified (patched) module object.

    ``add_patch`` can be called multiple times; patches will be applied
    sequentially.

    If ``module_name`` has already been imported, it is deleted from
    ``sys.modules`` so that it can be properly patched."""
    PATCHES[module_name].append(func)
    if module_name in sys.modules:
        del sys.modules[module_name]
