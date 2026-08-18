"""This module defines a utility for patching modules.

It was originally based on the recipe found in section 10.12 of the third
edition of the Python Cookbook but has been modified to work
with later Python versions."""

from collections import defaultdict
from importlib.abc import Loader, MetaPathFinder
from importlib.util import spec_from_file_location
import os.path
import sys

PATCHES = defaultdict(list)
FOUND_ONCE = set()


class PatchingFinder(MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        if fullname not in PATCHES:
            return None
        if fullname in FOUND_ONCE:
            return None
        if path is None or path == "":
            path = sys.path
        if "." in fullname:
            *parents, name = fullname.split(".")
        else:
            name = fullname
        for entry in path:
            if os.path.isdir(os.path.join(entry, name)):
                # this module has child modules
                filename = os.path.join(entry, name, "__init__.py")
                submodule_locations = [os.path.join(entry, name)]
            else:
                filename = os.path.join(entry, name + ".py")
                submodule_locations = None
            if not os.path.exists(filename):
                continue

            spec = spec_from_file_location(
                fullname,
                filename,
                loader=PatchingLoader(filename),
                submodule_search_locations=submodule_locations,
            )
            FOUND_ONCE.add(fullname)
            return spec

        return None  # we don't know how to import this


sys.meta_path.insert(0, PatchingFinder())


class PatchingLoader(Loader):
    def __init__(self, filename):
        self.filename = filename

    def create_module(self, spec):
        return None  # use default module creation semantics

    def exec_module(self, module):
        with open(self.filename) as f:
            data = f.read()
        exec(data, vars(module))
        for patch in PATCHES[module.__name__]:
            module = patch(module)


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
