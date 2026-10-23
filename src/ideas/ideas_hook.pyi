from types import ModuleType, CodeType
from typing import Callable, Sequence, Any
from importlib.abc import Loader, MetaPathFinder
import ast

from ideas import utils

class IdeasHook:
    callback_params: dict[str, Any] | None
    console_only: bool | None
    create_module: Callable[..., ModuleType] | None
    does_not_play_well_with_others: bool
    enabled: bool
    excluded_paths: list[str] | type[utils.DEFAULT] | None
    exec_: Callable[..., None] | None
    extensions: Sequence[str] | list[str]
    filename: str
    fullname: str
    loader: Loader
    meta_path_finder: MetaPathFinder
    module_class: type[Any] | None
    name: str
    parse_source: (
        Callable[[str, str, str], ast.Module]
        | Callable[[ast.Module], ast.Module]
        | None
    )
    source_init: Callable[[], str] | None
    source_module: ModuleType
    transform_ast: Callable[[ast.AST], ast.AST] | None
    transform_bytecode: Callable[[CodeType], CodeType] | None
    transform_source: Callable[[str], str] | None

    def __init__(
        self,
        callback_params: dict[str, Any] | None = None,
        console_only: bool = False,
        create_module: Callable[..., ModuleType] | None = None,
        does_not_play_well_with_others: bool = False,
        exec_: Callable[..., None] | None = None,
        extensions: Sequence[str] | None = None,
        excluded_paths: list[str] | type[utils.DEFAULT] | None = ...,
        name: str = "",
        module_class: type[Any] | None = None,
        parse_source: (
            Callable[[str, str, str], ast.Module]
            | Callable[[ast.Module], ast.Module]
            | None
        ) = None,
        source_init: Callable[[], str] | None = None,
        transform_ast: Callable[[ast.AST], ast.AST] | None = None,
        transform_bytecode: Callable[[CodeType], CodeType] | None = None,
        transform_source: Callable[[str], str] | None = None,
    ) -> None: ...
    def __repr__(self) -> str: ...
    def __eq__(self, other: object) -> bool: ...
