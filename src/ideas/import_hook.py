"""import_hook.py
------------------

This module contains the core functions required to create an import hook.
"""

import ast
import sys

from types import CodeType, ModuleType
from typing import Callable, Dict, Sequence, Optional, Any

from ideas import console
from ideas import utils
from ideas.ideas_hook import IdeasHook

from ideas import ideas_state
from ideas.finder import IdeasMetaPathFinder

# TODO: see if ipython_ast_node_transformer is needed


def create_hook(
    name: str = "",
    callback_params: Optional[Dict[str, Any]] = None,
    create_module: Optional[Callable[..., ModuleType]] = None,
    console_dict: Optional[Dict[str, Any]] = None,
    exec_: Optional[Callable[..., None]] = None,
    extensions: Optional[Sequence[str]] = None,
    excluded_paths: Optional[Sequence[str]] = utils.DEFAULT,
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
