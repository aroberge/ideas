"""This module contains the core functions required to create an import hook."""

import ast
import os
import sys

from importlib.abc import Loader, MetaPathFinder
from importlib.util import spec_from_file_location, decode_source

from . import console

Main_Module_Name = None

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

            ~/dir/file.py
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


class IdeasMetaFinder(MetaPathFinder):
    """A custom finder to locate modules.  The main reason for this code
       is to ensure that our custom loader, which does the code transformations,
       is used."""

    def __init__(
        self,
        callback_params=None,
        create_module=None,
        excluded_paths=None,
        exec_=None,
        extensions=None,
        module_class=None,
        transform_source=None,
        verbose_finder=False,
    ):
        self.verbose_finder = verbose_finder
        self.callback_params = callback_params
        self.custom_create_module = create_module
        self.excluded_paths = excluded_paths
        self.exec_ = exec_
        self.extensions = extensions
        self.module_class = module_class
        self.transform_source = transform_source

    def find_spec(self, fullname, path, target=None):
        """finds the appropriate properties (spec) of a module, and sets
           its loader."""
        if not path:
            return None

        if "." in fullname:
            name = fullname.split(".")[-1]
        else:
            name = fullname

        for entry in path:
            skip = False
            for sub_path in self.excluded_paths:
                if sub_path in entry.lower():
                    skip = True
                    if self.verbose_finder:
                        print("    Skipping over:", shorten_path(entry))
                    break
            if skip:
                continue

            for extension in self.extensions:
                if not extension.startswith("."):  # be forgiving ...
                    extension = "." + extension
                filename = os.path.join(entry, name + extension)

                if self.verbose_finder:
                    print(f"    Searching for {shorten_path(filename)}.")
                if os.path.exists(filename):
                    break
            else:
                continue

            if self.verbose_finder:
                print("->  Found: ", shorten_path(filename), "\n")
            return spec_from_file_location(
                fullname,
                filename,
                loader=IdeasLoader(
                    filename,
                    callback_params=self.callback_params,
                    create_module=self.custom_create_module,
                    exec_=self.exec_,
                    module_class=self.module_class,
                    transform_source=self.transform_source,
                ),
            )
        if self.verbose_finder:
            print(f"  IdeasMetaFinder did not find {shorten_path(fullname)}.\n")
        return None  # we don't know how to import this


class IdeasLoader(Loader):
    """A custom loader which will transform the source prior to its execution"""

    def __init__(
        self,
        filename,
        callback_params=None,
        create_module=None,
        exec_=None,
        module_class=None,
        transform_source=None,
    ):
        self.filename = filename
        self.exec_ = exec_
        self.callback_params = callback_params
        self.custom_create_module = create_module
        self.module_class = module_class
        self.transform_source = transform_source

    def create_module(self, spec):
        # Note: I do not have an example of custom module creation yet.
        if self.custom_create_module is not None:
            return self.custom_create_module(spec, callback_params=self.callback_params)
        else:
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
            raise e

        try:
            code_object = compile(tree, self.filename, "exec")
        except Exception as e:
            print("Exception raised while compiling tree.")
            raise e

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
                raise e


def create_hook(
    callback_params=None,
    create_module=None,
    console_dict=None,
    exec_=None,
    extensions=None,
    first=True,
    module_class=None,
    name=None,
    transform_source=None,
    verbose_finder=False,
):
    """Function to facilitate the creation of an import hook.

       It sets the parameters to be used by the import hook, and also
       does so for the interactive console.
    """
    if extensions is None:
        extensions = [".py"]

    excluded_paths = [PYTHON, IDEAS]

    if verbose_finder:
        print("Looking for files with extensions: ", extensions)
        print("The following paths will not be included in the search:")
        for sub_path in excluded_paths:
            print("  ", shorten_path(sub_path), "==", sub_path)

    hook = IdeasMetaFinder(
        callback_params=callback_params,
        create_module=create_module,
        excluded_paths=excluded_paths,
        exec_=exec_,
        extensions=extensions,
        module_class=module_class,
        transform_source=transform_source,
        verbose_finder=verbose_finder,
    )

    if first:
        sys.meta_path.insert(0, hook)
    else:
        sys.meta_path.append(hook)

    if transform_source is not None and isinstance(name, str):
        transform_source.__name__ = name
    console.configure(
        callback_params=callback_params,
        console_dict=console_dict,
        transform_source=transform_source,
    )

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
