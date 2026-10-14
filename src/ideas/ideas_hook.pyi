import ast
from types import CodeType, ModuleType
from typing import Callable, Dict, Sequence, Optional, Any, Union
from importlib.abc import Loader, MetaPathFinder

from ideas import utils

class IdeasHook:
    callback_params: dict[str, Any] | None
    console_only: bool | None
    create_module: Callable | None
    does_not_play_well_with_others: bool
    enabled: bool
    excluded_paths: list[str] | utils.DEFAULT | None
    exec_: Callable | None
    extensions: Sequence[str] | list[str]
    filename: str
    fullname: str
    loader: Loader
    meta_path_finder: MetaPathFinder
    module_class: type[Any] | None
    name: str
    parse_source: Callable | None
    source_init: Callable | None
    source_module: ModuleType
    transform_ast: Callable | None
    transform_bytecode: Callable | None
    transform_source: Callable | None

    def __init__(
        self,
        callback_params: Optional[Dict[str, Any]] = None,
        console_only: Optional[bool] = False,
        create_module: Optional[Callable[..., ModuleType]] = None,
        does_not_play_well_with_others: Optional[bool] = False,
        exec_: Optional[Callable[..., None]] = None,
        extensions: Optional[Sequence[str]] = None,
        excluded_paths: Union[Optional[Sequence[str]], utils.DEFAULT] = ...,
        name: str = "",
        module_class: Optional[type] = None,
        parse_source: Optional[Callable[[str, str, str], Optional[ast.AST]]] = None,
        source_init: Optional[Callable[[], str]] = None,
        transform_ast: Optional[Callable[[ast.AST], ast.AST]] = None,
        transform_bytecode: Optional[Callable[[CodeType], CodeType]] = None,
        transform_source: Optional[Callable[[str], str]] = None,
    ) -> None: ...
    def __repr__(self) -> str: ...
    def __eq__(self, other: object) -> bool: ...
