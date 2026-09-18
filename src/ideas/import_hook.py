"""import_hook.py
------------------

This module contains the core functions required to create an import hook.
"""

import ast
import os
import sys

from importlib.abc import Loader, MetaPathFinder
from importlib.util import spec_from_file_location, decode_source
from types import CodeType, ModuleType
from typing import Callable, Dict, Sequence, Optional, Any

from ideas import console
from ideas import utils
from ideas.ideas_hook import IdeasHook

from ideas import ideas_state


def verbose_finder(text):
    """Print some informative text when verbose is set"""
    if ideas_state.verbose:
        print(text)


# TODO: Add test for french_repeat
# TODO: Ensure that all existing hooks are tested.
# TODO: Refactor and clean-up the code


class IdeasMetaPathFinder(MetaPathFinder):  # pylint: disable=R0902
    """A custom finder to locate modules. The main reason for this code is
    to ensure that our custom loader, which does the code transformations,
    is used.

    This single metapath finder is meant to cover all existing examples
    and has become nearly unreadable. It definitely needs a serious rewrite.
    """

    def __init__(self, ideas_hook=None):
        self.ideas_hook = ideas_hook
        if self.ideas_hook is None:
            raise RuntimeError("IdeasHook instance missing in IdeasMetaPathFinder().")
        self.inform_about_all_possible_paths = True

    def __repr__(self):
        return f"<IdeasMetaPathFinder for {self.ideas_hook.name}>"

    def find_spec(self, fullname, path, target=None):  # pylint: disable=W0613
        """finds the appropriate properties (spec) of a module, and sets
        its loader."""
        if not self.ideas_hook.enabled:
            verbose_finder(
                f"Hook {self.ideas_hook.name} disabled in IdeasMetaPathFinder."
            )
            return None

        # avoid lots of spurious print statements when running verbose tests
        if fullname == "pygments":
            return None

        verbose_finder(f"\n{self.ideas_hook.name}: inside find_spec")

        if not path:
            path = [os.getcwd()] + sys.path

        if self.inform_about_all_possible_paths:  # Do only once
            verbose_finder(
                "The following paths *might* be searched as they are in sys.path:"
            )
            for p in path:
                verbose_finder(f"    {utils.shorten_path(p)}")
            if self.ideas_hook.excluded_paths:
                verbose_finder(
                    "The following have been set as 'excluded' for this import hook."
                )
                for p in self.ideas_hook.excluded_paths:
                    verbose_finder(f"    {utils.shorten_path(p)}")
            self.inform_about_all_possible_paths = False

        if "." in fullname:
            module_name = fullname.split(".")[-1]
        else:
            module_name = fullname

        for entry in path:
            skip = False
            for sub_path in self.ideas_hook.excluded_paths:
                if entry.lower().startswith(sub_path.lower()):
                    skip = True
                    verbose_finder(f"Skipping over: {utils.shorten_path(entry)}")
                    break
            if skip:
                continue

            for extension in self.ideas_hook.extensions:
                if not extension.startswith("."):  # be forgiving ...
                    extension = "." + extension
                filename = os.path.join(entry, module_name + extension)

                verbose_finder(f"Searching for {utils.shorten_path(filename)}")
                if os.path.exists(filename):
                    verbose_finder(f"Found: {utils.shorten_path(filename)}\n")
                    break
                verbose_finder(
                    "    IdeasMetaPathFinder did not find "
                    + f"{utils.shorten_path(fullname)}\n",
                )
            else:
                continue

            return spec_from_file_location(
                fullname,
                filename,
                loader=IdeasLoader(
                    filename,
                    ideas_hook=self.ideas_hook,
                    callback_params=self.ideas_hook.callback_params,
                    create_module=self.ideas_hook.create_module,
                    exec_=self.ideas_hook.exec_,
                    module_class=self.ideas_hook.module_class,
                    source_init=self.ideas_hook.source_init,
                    transform_ast=self.ideas_hook.transform_ast,
                    transform_bytecode=self.ideas_hook.transform_bytecode,
                    parse_source=self.ideas_hook.parse_source,
                ),
            )

        verbose_finder(f"{self.__repr__()} cannot import {fullname}\n")

        return self.basic_find_spec(fullname=fullname, path=path, target=None)
        # return None  # we don't know how to import this

    def basic_find_spec(self, fullname, path, target=None):

        if fullname in utils.std_lib_names:  # Avoid circular imports for some hooks
            return None
        if path is None or path == "":
            path = [os.getcwd()]  # top level import --
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

            return spec_from_file_location(
                fullname,
                filename,
                loader=IdeasLoader(
                    filename,
                    ideas_hook=self.ideas_hook,
                    callback_params=self.ideas_hook.callback_params,
                    create_module=self.ideas_hook.create_module,
                    exec_=self.ideas_hook.exec_,
                    module_class=self.ideas_hook.module_class,
                    source_init=self.ideas_hook.source_init,
                    transform_ast=self.ideas_hook.transform_ast,
                    transform_bytecode=self.ideas_hook.transform_bytecode,
                    parse_source=self.ideas_hook.parse_source,
                ),
                submodule_search_locations=submodule_locations,
            )

        return None  # we don't know how to import this


class IdeasLoader(Loader):  # pylint: disable=R0902
    """A custom loader which will transform the source prior to its execution

    While not as bad as the code used in the current metapath finder,
    it also needs to be rewritten to be more readable.
    """

    def __init__(
        self,
        filename,
        ideas_hook=None,
        callback_params=None,
        create_module=None,
        exec_=None,
        module_class=None,
        source_init=None,
        transform_ast=None,
        transform_bytecode=None,
        parse_source=None,
    ):  # pylint: disable=R0913
        self.filename = filename
        self.ideas_hook = ideas_hook
        self.exec_ = exec_
        self.callback_params = callback_params
        self.custom_create_module = create_module
        self.module_class = module_class
        self.source_init = source_init
        self.transform_ast = transform_ast
        self.transform_bytecode = transform_bytecode
        self.parse_source = parse_source

    def create_module(self, spec):
        """Potential replacement for the default create_module method."""
        # Note: I do not have an example of custom module creation yet.
        if self.custom_create_module is not None:
            return self.custom_create_module(spec, callback_params=self.callback_params)
        return None  # use default module creation semantics

    def exec_module(self, module):
        """Import the source code, transform it before executing it so that
        it is known to Python.
        """
        if (
            module.__name__ == ideas_state.source_argument
            and ideas_state.run_as_main_argument
        ):
            module.__name__ = "__main__"

        if self.module_class is not None:
            module.__class__ = self.module_class  # pylint: disable=E0243

        with open(self.filename, mode="rb") as file:
            encoded_source = file.read()
        source = decode_source(encoded_source)
        original_source = source

        source = ideas_state.source_transforms(
            source,
            filename=self.filename,
            module=module,
            callback_params=self.callback_params,
        )

        if ideas_state.show_changes and original_source != source:
            ideas_state.print_source(
                original_source,
                header=f"Original source from {utils.shorten_path(self.filename)}",
            )
            ideas_state.print_source(source, header="Transformed source")

        if self.source_init is not None:
            source = self.source_init() + source

        parse_source = self.parse_source or ast.parse
        try:
            tree = parse_source(source, self.filename, "exec")
        except Exception:
            if ideas_state.verbose:
                print("An exception was raised while attempting to produce an AST.")
            raise

        if self.transform_ast is not None:
            tree = self.transform_ast(tree)

        try:
            code_object = compile(tree, self.filename, "exec")
        except Exception:
            if ideas_state.verbose:
                print("An exception was raised while attempting to produce an AST.")
            raise

        if self.transform_bytecode is not None:
            try:
                code_object = self.transform_bytecode(code_object)
            except Exception:
                if ideas_state.verbose:
                    print(
                        "An exception was raised while trying to modify the bytecode."
                    )
                raise

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
                exec(code_object, module.__dict__)  # pylint: disable=W0122
            except Exception:
                if ideas_state.verbose:
                    print(
                        "An exception was raised while attempting to execute the code object."
                    )
                raise


def create_hook(
    name: str = "",
    callback_params: Optional[Dict[str, Any]] = None,
    create_module: Optional[Callable[..., ModuleType]] = None,
    console_dict: Optional[Dict[str, Any]] = None,
    exec_: Optional[Callable[..., None]] = None,
    extensions: Optional[Sequence[str]] = None,
    excluded_paths: Optional[Sequence[str]] = utils.DEFAULT,
    first: bool = True,
    ipython_ast_node_transformer: Optional[ast.NodeTransformer] = None,
    module_class: Optional[type] = None,
    source_init: Optional[Callable[[], str]] = None,
    transform_ast: Optional[Callable[[ast.AST], ast.AST]] = None,
    transform_bytecode: Optional[Callable[[CodeType], CodeType]] = None,
    transform_source: Optional[Callable[[str], str]] = None,
    parse_source: Optional[Callable[[str, str, str], Optional[ast.AST]]] = None,
) -> IdeasHook:  # pylint: disable=R0913,R0914
    """Function to facilitate the creation of an import hook.

    ``name``: required parameter which must be the ``__name__`` of
    the module in which the import hook is defined.

    Each of the following parameter is optional; most of these are
    never needed except in some unusual import hooks.

    Usually, at least one of ``transform_ast``, ``transform_bytecode``s,
    and ``transform_source`` should be specified.

    * ``callback_params``: a dict containing keyword parameters
      to be passed back to the ``transform_source`` function.
    * ``create_module``: a custom function to create a module object
      instead of using Python's default.
    * ``console_dict``: a dict object used as 'locals' with the Ideas console,
      instead of its usual default.
    * ``exec_``: a custom method used to execute the source code inside
      a module's dict.
    * ``extensions``: a list of file extensions, other than the usual `.py`, etc.,
      used to identify modules containing source code.
    * ``excluded_paths``: a list of paths, written as strings,
      to be excluded for consideration.
      If using the default argument, excluded paths include the location of the standard
      library, the site packages, as well as files from this project.
      If the argument is None, this becomes an empty list.
    * ``ipython_ast_node_transformer``: used to do AST transformations in an
      IPython/Jupyter environment. It should be a class derived from
      ``ast.NodeTransformer`` and return a ``node``.
    * ``module_class``: custom class to use for the module created instead of
      the default one assigned by Python.
    * ``source_init``: custom code to be executed before any code from
      a user is executed. For example, if one creates an import hook that
      treats every ``float`` as a ``Decimal`` object, this custom code
      could be::

          from decimal import Decimal

    * ``transform_ast``: used to do AST transformations in a Python
      environment (excluding IPython/Jupyter).  It should be a class
      derived from ``ast.NodeTransformer``, eventually returning a
      tree object.
    * ``transform_bytecode``: used to mutate a code object.
    * ``transform_source``: used to transform some source code prior
      to execution.

    Returns: an IdeasHook instance.
    """

    if not name:
        raise RuntimeError(
            "`name` is required and should be the source module __name__."
        )

    hook = IdeasHook(
        callback_params=callback_params,
        create_module=create_module,
        excluded_paths=excluded_paths,
        exec_=exec_,
        extensions=extensions,
        name=name,
        module_class=module_class,
        source_init=source_init,
        transform_ast=transform_ast,
        transform_bytecode=transform_bytecode,
        transform_source=transform_source,
        parse_source=parse_source,
    )
    ideas_state._add_hook(hook)
    hook.meta_path_finder = IdeasMetaPathFinder(ideas_hook=hook)

    # By default, we insert our hook before those included by Python
    # so that it is used. If more than one hook is used,
    # the order is first added, last used (only if others fail before)
    sys.meta_path.insert(0, hook.meta_path_finder)

    if ideas_state.verbose and extensions is not None:
        print("Looking for files with extensions: ", extensions)
        print("The following paths will not be included in the search:")
        for sub_path in hook.excluded_paths:
            print("  ", utils.shorten_path(sub_path), sub_path)

    ## ----- Setting up Ideas Interactive Console

    console.configure(
        callback_params=callback_params,
        console_dict=console_dict,
        transform_ast=transform_ast,
        transform_bytecode=transform_bytecode,
        parse_source=parse_source,
    )

    ## ----- Conditionally setting up IPython shell including Jupyter Notebooks
    if source_init is not None:
        ideas_state._console_source_inits.append(source_init)
    try:
        ipython_shell = get_ipython()  # type: ignore # noqa
    except NameError:
        pass
    else:
        from ideas.ipython_utils import set_up_ipython_shell

        set_up_ipython_shell(
            ipython_shell,
            ipython_ast_node_transformer=ipython_ast_node_transformer,
            source_init=source_init,
            transform_source=transform_source,
        )

    return hook
