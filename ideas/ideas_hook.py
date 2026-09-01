import ast
import sys
from types import CodeType, ModuleType
from typing import Callable, Dict, Sequence, Optional, Any

from . import utils


class IdeasHook:
    """A custom import hook main object."""

    def __init__(
        self,
        callback_params: Optional[Dict[str, Any]] = None,
        create_module: Optional[Callable[..., ModuleType]] = None,
        exec_: Optional[Callable[..., None]] = None,
        extensions: Optional[Sequence[str]] = None,
        excluded_paths: Optional[Sequence[str]] = utils.DEFAULT,
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
        if excluded_paths is utils.DEFAULT:
            self.excluded_paths = []
        elif excluded_paths is None:
            self.excluded_paths = []
        else:
            self.excluded_paths = excluded_paths
        self.exec_ = exec_
        self.extensions = extensions if extensions is not None else [".py"]
        self.name = name
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

    def __eq__(self, other):
        return isinstance(other, IdeasHook) and self.name == other.name
