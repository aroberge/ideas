"""This is a simple proof of concept. It is not meant to be taken seriously."""

import os
import sys

from importlib.abc import Loader, MetaPathFinder
from importlib.util import spec_from_file_location

Main_Module_Name = None
stdlib_dir = os.path.dirname(os.__file__)


class MyMetaFinder(MetaPathFinder):
    """A custom finder to locate modules.  The main reason for this code
       is to ensure that our custom loader, which does the code transformations,
       is used."""

    def __init__(self, module_class=None, source_transformer=None, module_dict=None):
        self.module_class = module_class
        self.source_transformer = source_transformer
        self.module_dict = module_dict

    def find_spec(self, fullname, path, target=None):
        """finds the appropriate properties (spec) of a module, and sets
           its loader."""
        if not path:
            path = [os.getcwd()]
        if "." in fullname:
            name = fullname.split(".")[-1]
        else:
            name = fullname
        for entry in path:
            if stdlib_dir in entry:  # do not process files from standard Library
                continue
            if os.path.isdir(os.path.join(entry, name)):
                # this module has child modules
                filename = os.path.join(entry, name, "__init__.py")
                submodule_locations = [os.path.join(entry, name)]
            else:
                filename = os.path.join(entry, name + ".py")
                submodule_locations = None
            if not os.path.exists(filename):
                continue

            return spec_from_file_location(
                fullname,
                filename,
                loader=MyLoader(
                    filename,
                    module_class=self.module_class,
                    source_transformer=self.source_transformer,
                    module_dict=self.module_dict,
                ),
                submodule_search_locations=submodule_locations,
            )
        return None  # we don't know how to import this


class MyLoader(Loader):
    """A custom loader which will transform the source prior to its execution"""

    def __init__(
        self, filename, module_class=None, source_transformer=None, module_dict=None
    ):
        self.filename = filename
        self.module_class = module_class
        self.source_transformer = source_transformer
        self.module_dict = module_dict

    def create_module(self, spec):
        return None  # use default module creation semantics

    def exec_module(self, module):
        """Import the source code, transform it before executing it so that
           it is known to Python."""
        global Main_Module_Name

        with open(self.filename) as f:
            source = f.read()

        if self.module_class is not None:
            module.__class__ = self.module_class

        if Main_Module_Name is not None:
            sys.modules["__main__"] = sys.modules[module.__name__]
            module.__name__ = "__main__"
            Main_Module_Name = None

        if self.source_transformer is not None:
            source = self.source_transformer(source, filename=self.filename)

        mod_dict = sys.modules[module.__name__].__dict__
        if self.module_dict is None:
            exec(source, mod_dict)
        else:
            self.module_dict = self.module_dict(self.filename)
            self.module_dict.update(mod_dict)
            exec(source, self.module_dict)
            mod_dict.update(self.module_dict)


def create_hook(module_class=None, source_transformer=None, module_dict=None):
    """Function to facilitate the creation of an import hook"""
    return MyMetaFinder(
        module_class=module_class,
        source_transformer=source_transformer,
        module_dict=module_dict,
    )


def remove_hook(hook):
    """Function used to remove a previously import hook inserted in sys.meta_path"""
    for index, h in enumerate(sys.meta_path):
        if h == hook:
            break
    else:
        print("Import hook not found in remove_hook.")
        return
    del sys.meta_path[index]


if __name__ == "__main__":
    if len(sys.argv) > 1:
        Main_Module_Name = sys.argv[-1]
        print("__main__ is", Main_Module_Name)
        __import__(Main_Module_Name)
        sys.modules["constants"] = sys.modules["__main__"]
        __name__ = "constants"
