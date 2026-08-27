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

from . import console
from . import session
from . import utils


def finder_inform(text):
    """Print some informative text when verbose finder is set"""
    if session.current_state.verbose_finder:
        print(text)


DEFAULT = object()

# TODO: Add test for french_repeat
# TODO: Ensure that all existing hooks are tested.


class IdeasHook:
    """A custom import hook main object."""

    def __init__(
        self,
        callback_params: Optional[Dict[str, Any]] = None,
        create_module: Optional[Callable[..., ModuleType]] = None,
        exec_: Optional[Callable[..., None]] = None,
        extensions: Optional[Sequence[str]] = None,
        excluded_paths: Optional[Sequence[str]] = DEFAULT,
        name: Optional[str] = None,
        module_class: Optional[type] = None,
        parse_source: Optional[Callable[[str, str, str], Optional[ast.AST]]] = None,
        source_init: Optional[Callable[[], str]] = None,
        transform_ast: Optional[Callable[[ast.AST], ast.AST]] = None,
        transform_bytecode: Optional[Callable[[CodeType], CodeType]] = None,
        transform_source: Optional[Callable[[str], str]] = None,
    ):
        self.callback_params = callback_params
        self.create_module = create_module
        if excluded_paths is DEFAULT:
            self.excluded_paths = [utils.PYTHON, utils.IDEAS, utils.SITE_PACKAGES]
        elif excluded_paths is None:
            self.excluded_paths = []
        self.exec_ = exec_
        self.extensions = extensions if extensions is not None else [".py"]
        self.name = name if name is not None else utils.generate_variable_names()
        self.module_class = module_class
        self.parse_source = parse_source
        self.source_init = source_init
        self.transform_ast = transform_ast
        self.transform_bytecode = transform_bytecode
        self.transform_source = transform_source

        # The following attribute are created by the IdeasMetaFinder
        self.meta_path_finder = None  # IdeasMetaFinder instance; is it
        self.filename = None
        self.fullname = None
        self.loader = None  # Is this needed?
        # This will normally be changed via a method from session.current_state in session.py
        self.enabled = True

        try:
            self.source_module = sys.modules[name]
        except KeyError:
            print("FATAL ERROR!")
            print(
                "IdeasHook object must be created with the name of its source module."
            )
            raise

    def __repr__(self):
        return f"<Ideas import hook: {self.name}>"


class IdeasMetaFinder(MetaPathFinder):  # pylint: disable=R0902
    """A custom finder to locate modules. The main reason for this code
    is to ensure that our custom loader, which does the code transformations,
    is used."""

    def __init__(self, ideas_hook=None):  # pylint: disable=R0913
        self.ideas_hook = ideas_hook

    def find_spec(self, fullname, path, target=None):  # pylint: disable=W0613
        """finds the appropriate properties (spec) of a module, and sets
        its loader."""
        if self.ideas_hook is None:
            print("WARNING: No IdeasHook object was passed.")
            return None

        if not self.ideas_hook.enabled:
            print(f"Hook {self.ideas_hook.name} disabled in IdeasMetaPathFinder.")
            return None

        if not path:
            path = [os.getcwd()]

        if "." in fullname:
            module_name = fullname.split(".")[-1]
        else:
            module_name = fullname

        for entry in path:
            skip = False
            for sub_path in self.ideas_hook.excluded_paths:
                if sub_path in entry.lower():
                    skip = True
                    if session.current_state.verbose_finder:
                        print("    Skipping over:", utils.shorten_path(entry))
                    break
            if skip:
                continue

            for extension in self.ideas_hook.extensions:
                if not extension.startswith("."):  # be forgiving ...
                    extension = "." + extension
                filename = os.path.join(entry, module_name + extension)

                finder_inform(
                    f"    Searching for {utils.shorten_path(filename)}{extension}"
                )
                if os.path.exists(filename):
                    finder_inform(
                        f"    Found: {utils.shorten_path(filename) + extension}\n"
                    )
                    break
                finder_inform(
                    "    IdeasMetaFinder did not find"
                    + f"{utils.shorten_path(fullname)}{extension}\n",
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
                    transform_source=self.ideas_hook.transform_source,
                    parse_source=self.ideas_hook.parse_source,
                ),
            )
        return None  # we don't know how to import this


class IdeasLoader(Loader):  # pylint: disable=R0902
    """A custom loader which will transform the source prior to its execution"""

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
        transform_source=None,
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
        self.transform_source = transform_source
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
        if module.__name__ == session.current_state.source_argument:
            module.__name__ = "__main__"
            session.current_state.source_argument = None

        if self.module_class is not None:
            module.__class__ = self.module_class  # pylint: disable=E0243

        with open(self.filename, mode="rb") as file:
            encoded_source = file.read()
        source = decode_source(encoded_source)
        original_source = source

        if self.transform_source is not None:
            source = self.transform_source(
                source,
                filename=self.filename,
                module=module,
                callback_params=self.callback_params,
            )

        if session.current_state.show_changes and original_source != source:
            utils.print_source(original_source, header="Original")
            utils.print_source(source, header="New")

        if self.source_init is not None:
            source = self.source_init() + source

        parse_source = self.parse_source or ast.parse
        try:
            tree = parse_source(source, self.filename, "exec")
        except Exception:
            print("Exception raised while parsing source.")
            raise

        if self.transform_ast is not None:
            tree = self.transform_ast(tree)

        try:
            code_object = compile(tree, self.filename, "exec")
        except Exception:
            print("Exception raised while compiling tree.")
            raise

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
                exec(code_object, module.__dict__)  # pylint: disable=W0122
            except Exception:
                print("Exception raised while executing code object.")
                raise


def create_hook(
    name: str = "",
    callback_params: Optional[Dict[str, Any]] = None,
    create_module: Optional[Callable[..., ModuleType]] = None,
    console_dict: Optional[Dict[str, Any]] = None,
    exec_: Optional[Callable[..., None]] = None,
    extensions: Optional[Sequence[str]] = None,
    excluded_paths: Optional[Sequence[str]] = DEFAULT,
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
    * ``excluded_paths``: a list of paths to be excluded for consideration.
      If not specified, excluded paths include the location of the standard
      library, the site packages, as well as files from this project.
    * ``first``: if ``True``, the custom hook will be used as the first
      location in ``sys.meta_path``, to look for source files.
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
    """

    if not name:
        raise RuntimeError(
            "`name` is required and should be the source module __name__."
        )

    ideas_hook = IdeasHook(
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
    session.current_state.add_hook(ideas_hook)
    ideas_hook.meta_path_finder = IdeasMetaFinder(ideas_hook=ideas_hook)

    if first:
        sys.meta_path.insert(0, ideas_hook.meta_path_finder)
    else:
        sys.meta_path.append(ideas_hook.meta_path_finder)

    if session.current_state.verbose_finder:
        print("Looking for files with extensions: ", extensions)
        print("The following paths will not be included in the search:")
        for sub_path in ideas_hook.excluded_paths:
            print("  ", utils.shorten_path(sub_path), sub_path)

    ## ----- Setting up Ideas Interactive Console

    console.configure(
        callback_params=callback_params,
        console_dict=console_dict,
        source_init=source_init,
        transform_ast=transform_ast,
        transform_bytecode=transform_bytecode,
        transform_source=transform_source,
        parse_source=parse_source,
    )

    ## ----- Conditionally setting up IPython shell including Jupyter Notebooks
    try:
        ipython_shell = get_ipython()  # noqa
    except NameError:
        pass
    else:
        set_up_ipython_shell(
            ipython_shell,
            ipython_ast_node_transformer=ipython_ast_node_transformer,
            source_init=source_init,
            transform_source=transform_source,
        )

    return ideas_hook


def set_up_ipython_shell(
    ipython_shell,
    ipython_ast_node_transformer=None,
    source_init=None,
    transform_source=None,
):
    if transform_source is not None:
        ipython_source_transformer = make_ipython_source_transformer(transform_source)
        ipython_shell.input_transformers_cleanup.append(ipython_source_transformer)

    if source_init is not None and source_init().strip():
        print("   The following initializing code from ideas is included:\n")
        print(source_init().strip())
        lines = [line for line in source_init().splitlines() if line.strip()]
        for line in lines:
            ipython_shell.ex(line)

    if ipython_ast_node_transformer is not None:
        wrapped_ipython_ast_node_transformer = make_ipython_ast_node_transformer(
            ipython_ast_node_transformer
        )
        ipython_shell.ast_transformers.append(wrapped_ipython_ast_node_transformer())


def make_ipython_source_transformer(transform_source):
    """Takes a source transform and makes returns an IPython compatible
    source transformer.
    """

    # This is done as during the cleanup phase
    # (``ipython_shell.input_transformers_cleanup``), as opposed to the
    # post phase (``ipython_shell.input_transformers_post``) so that
    # transformations that work on code blocks (such as ``repeat``)
    # can work properly.
    def ipython_source_transformer(lines):  # noqa
        # In IPython, the source transformation operates on a list of lines
        original_source = "".join(lines)
        source = transform_source(original_source)
        if session.current_state.show_changes and source != original_source:
            session.current_state.print_transformed(source, header="New: ")
        lines = source.splitlines(keepends=True)
        return lines

    return ipython_source_transformer


def make_ipython_ast_node_transformer(ipython_ast_node_transformer):
    """Takes an AST transformer designed to work with IPython,
    and wraps it to add a warning in case the user would like to
    see how the code is actually transformed, since this is not
    possible when using IPython.
    """

    def wrapped_ipython_ast_node_transformer():
        if session.current_state.show_changes:
            print(
                "Cannot show the changed source for AST transform in IPython/Jupyter."
            )
            session.current_state.show_changes = False
        return ipython_ast_node_transformer

    return wrapped_ipython_ast_node_transformer


def remove_hook(hook):
    """Function used to remove a previously imported hook inserted in sys.meta_path"""
    for index, meta_finder in enumerate(sys.meta_path):
        if meta_finder == hook:
            del sys.meta_path[index]
            break
    else:
        print("Import hook not found in remove_hook.")
        return
