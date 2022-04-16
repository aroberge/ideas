"""import_hook.py
------------------

This module contains the core functions required to create an import hook.
"""

import ast
import os
import sys

from importlib.abc import Loader, MetaPathFinder
from importlib.util import spec_from_file_location, decode_source

from . import console
from .utils import shorten_path, PYTHON, IDEAS, SITE_PACKAGES


# Identify the main script assuming that it has been called from
# the command line using something like
# python -m ideas main_script[.py] -some_flag
MAIN_NAME = None
if len(sys.argv) > 1 and not sys.argv[1].startswith("-"):
    MAIN_NAME = sys.argv[1].rstrip(".py")


class IdeasMetaFinder(MetaPathFinder):
    """A custom finder to locate modules. The main reason for this code
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
        source_init=None,
        transform_ast=None,
        transform_bytecode=None,
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
        self.source_init = source_init
        self.transform_ast = transform_ast
        self.transform_bytecode = transform_bytecode
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
                    source_init=self.source_init,
                    transform_ast=self.transform_ast,
                    transform_bytecode=self.transform_bytecode,
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
        source_init=None,
        transform_ast=None,
        transform_bytecode=None,
        transform_source=None,
    ):
        self.filename = filename
        self.exec_ = exec_
        self.callback_params = callback_params
        self.custom_create_module = create_module
        self.module_class = module_class
        self.source_init = source_init
        self.transform_ast = transform_ast
        self.transform_bytecode = transform_bytecode
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
        # The main script should be the very first one imported.
        # To avoid potential named conflicts, we ensure that the potential
        # identification is only done once.
        global MAIN_NAME
        if module.__name__ is not None and module.__name__ == MAIN_NAME:
            module.__name__ = "__main__"
        MAIN_NAME = None

        if self.module_class is not None:
            module.__class__ = self.module_class

        with open(self.filename, mode="r+b") as f:
            source = decode_source(f.read())

        if self.transform_source is not None:
            source = self.transform_source(
                source,
                filename=self.filename,
                globals_=module.__dict__,
                module=module,
                callback_params=self.callback_params,
            )

        if self.source_init is not None:
            source = self.source_init() + source

        try:
            tree = ast.parse(source, self.filename)
        except Exception as e:
            print("Exception raised while parsing source.")
            raise e

        if self.transform_ast is not None:
            tree = self.transform_ast(tree)

        try:
            code_object = compile(tree, self.filename, "exec")
        except Exception as e:
            print("Exception raised while compiling tree.")
            raise e

        if self.transform_bytecode is not None:
            code_object = self.transform_bytecode(code_object)

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
    ipython_ast_node_transformer=None,
    callback_params=None,
    create_module=None,
    console_dict=None,
    exec_=None,
    extensions=None,
    first=True,
    module_class=None,
    hook_name=None,
    source_init=None,
    transform_ast=None,
    transform_bytecode=None,
    transform_source=None,
    verbose_finder=False,
):
    """Function to facilitate the creation of an import hook.

    It sets the parameters to be used by the import hook, and also
    does so for the interactive console.
    """
    if extensions is None:
        extensions = [".py"]

    excluded_paths = [PYTHON, IDEAS, SITE_PACKAGES]

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
        source_init=source_init,
        transform_ast=transform_ast,
        transform_bytecode=transform_bytecode,
        transform_source=transform_source,
        verbose_finder=verbose_finder,
    )

    if first:
        sys.meta_path.insert(0, hook)
    else:
        sys.meta_path.append(hook)

    for obj in [transform_source, transform_ast, transform_bytecode, source_init]:
        if obj is not None and isinstance(hook_name, str):
            obj._hook_name_ = hook_name

    console.configure(
        callback_params=callback_params,
        console_dict=console_dict,
        source_init=source_init,
        transform_ast=transform_ast,
        transform_bytecode=transform_bytecode,
        transform_source=transform_source,
    )
    if transform_source is not None:
        try:
            ip = get_ipython()  # noqa
            ipython_source_transformer = make_ipython_source_transformer(
                transform_source
            )
            ip.input_transformers_post.append(ipython_source_transformer)
        except NameError:
            pass

    if ipython_ast_node_transformer is not None:
        try:
            ip = get_ipython()  # noqa
            ip.ast_transformers.append(ipython_ast_node_transformer)
        except NameError:
            pass

    return hook


def make_ipython_source_transformer(transform_source):
    def ipython_source_transformer(lines):
        source = "".join(lines)
        source = transform_source(source)
        lines = source.splitlines(keepends=True)
        return lines

    return ipython_source_transformer


def remove_hook(hook):
    """Function used to remove a previously imported hook inserted in sys.meta_path"""
    for index, h in enumerate(sys.meta_path):
        if h == hook:
            break
    else:
        print("Import hook not found in remove_hook.")
        return
    del sys.meta_path[index]
    console.configure()
