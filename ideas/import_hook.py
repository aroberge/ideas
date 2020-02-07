"""This module contains the core functions required to create an import hook."""

import ast
import os
import sys

from importlib.abc import Loader, MetaPathFinder
from importlib.util import spec_from_file_location, decode_source

from . import console

Main_Module_Name = None
stdlib_dir = os.path.dirname(os.__file__)

# N.B. While I was able to play with import hooks using the deprecated
# imp module (which still exists), I couldn't quite figure out how to
# do it using the recommended importlib package. I got the required
# information after asking a question on StackOverflow which lead
# to this answer https://stackoverflow.com/a/43573798/558799.
# I used the code provided as my starting point for the code written below.


class IdeasMetaFinder(MetaPathFinder):
    """A custom finder to locate modules.  The main reason for this code
       is to ensure that our custom loader, which does the code transformations,
       is used."""

    def __init__(
        self,
        callback_params=None,
        exec_=None,
        extensions=None,
        module_class=None,
        transform_source=None,
    ):
        self.callback_params = callback_params
        self.exec_ = exec_
        if extensions is None:
            self.extensions = [".py", ".pyw"]
        else:
            self.extensions = extensions
        self.module_class = module_class
        self.transform_source = transform_source

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
                if not os.path.exists(filename):
                    continue
            else:
                for extension in self.extensions:
                    if not extension.startswith("."):  # be forgiving ...
                        extension = "." + extension
                    filename = os.path.join(entry, name + extension)

                    submodule_locations = None
                    if os.path.exists(filename):
                        break
                else:
                    continue

            return spec_from_file_location(
                fullname,
                filename,
                loader=IdeasLoader(
                    filename,
                    module_class=self.module_class,
                    transform_source=self.transform_source,
                    exec_=self.exec_,
                    callback_params=self.callback_params,
                ),
                submodule_search_locations=submodule_locations,
            )
        return None  # we don't know how to import this


class IdeasLoader(Loader):
    """A custom loader which will transform the source prior to its execution"""

    def __init__(
        self,
        filename,
        module_class=None,
        transform_source=None,
        exec_=None,
        callback_params=None,
    ):
        self.filename = filename
        self.module_class = module_class
        self.transform_source = transform_source
        self.exec_ = exec_
        self.callback_params = callback_params

    def create_module(self, spec):
        return None  # use default module creation semantics

    def exec_module(self, module):
        """Import the source code, transform it before executing it so that
           it is known to Python.
        """
        global Main_Module_Name

        if self.module_class is not None:
            module.__class__ = self.module_class

        with open(self.filename, mode="r+b") as f:
            source = decode_source(f.read())

        if Main_Module_Name is not None:
            sys.modules["__main__"] = sys.modules[module.__name__]
            module.__name__ = "__main__"
            Main_Module_Name = None

        if self.transform_source is not None:
            source = self.transform_source(
                source,
                filename=self.filename,
                globals_=module.__dict__,
                module=module,
                callback_params=self.callback_params,
            )

        try:
            tree = ast.parse(source, self.filename)
        except Exception as e:
            print("Exception raised while parsing source.")
            print(e)

        try:
            code_object = compile(tree, self.filename, "exec")
        except Exception as e:
            print("Exception raised while compiling tree.")
            print(e)

        if self.exec_ is not None:
            self.exec_(
                code_object,
                filename=self.filename,
                globals_=module.__dict__,
                module=module,
                callback_params=self.callback_params,
            )
        else:
            try:
                exec(code_object, module.__dict__)
            except Exception as e:
                print("Exception raised while executing code object.")
                print(e)


def create_hook(
    callback_params=None,
    console_dict=None,
    exec_=None,
    extensions=None,
    first=True,
    module_class=None,
    name=None,
    transform_source=None,
):
    """Function to facilitate the creation of an import hook.

       It sets the parameters to be used by the import hook, and also
       does so for the interactive console.
    """

    # We do not include module_class in the console configuration as
    # it has no module to be instantiated.
    if transform_source is not None and isinstance(name, str):
        transform_source.__name__ = name
    console.configure(
        callback_params=callback_params,
        console_dict=console_dict,
        transform_source=transform_source,
    )

    hook = IdeasMetaFinder(
        callback_params=callback_params,
        exec_=exec_,
        extensions=extensions,
        module_class=module_class,
        transform_source=transform_source,
    )

    if first:
        sys.meta_path.insert(0, hook)
    else:
        sys.meta_path.append(hook)

    return hook


def remove_hook(hook):
    """Function used to remove a previously import hook inserted in sys.meta_path"""
    for index, h in enumerate(sys.meta_path):
        if h == hook:
            break
    else:
        print("Import hook not found in remove_hook.")
        return
    del sys.meta_path[index]
    console.configure()


def import_as_main(module):
    raise NotImplementedError
