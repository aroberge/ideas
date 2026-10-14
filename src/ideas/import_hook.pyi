import ast
import sys
from types import CodeType, ModuleType
from typing import Callable, Dict, Sequence, Optional, Any
from ideas import console
from ideas import utils
from ideas.ideas_hook import IdeasHook
from ideas import ideas_state
from ideas.finder import IdeasMetaPathFinder

def create_hook(
    name: str = "",
    callback_params: Optional[Dict[str, Any]] = None,
    console_only: Optional[bool] = False,
    create_module: Optional[Callable[..., ModuleType]] = None,
    console_dict: Optional[Dict[str, Any]] = None,
    does_not_play_well_with_others: Optional[bool] = False,
    exec_: Optional[Callable[..., None]] = None,
    extensions: Optional[Sequence[str]] = None,
    excluded_paths: Optional[Sequence[str]] = ...,
    ipython_ast_node_transformer: Optional[ast.NodeTransformer] = None,
    module_class: Optional[type] = None,
    source_init: Optional[Callable[[], str]] = None,
    transform_ast: Optional[Callable[[ast.AST], ast.AST]] = None,
    transform_bytecode: Optional[Callable[[CodeType], CodeType]] = None,
    transform_source: Optional[Callable[[str], str]] = None,
    parse_source: Optional[Callable[[str, str, str], Optional[ast.AST]]] = None,
) -> Optional[IdeasHook]: ...
