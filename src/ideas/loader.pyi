from typing import Callable, Any
from types import ModuleType, CodeType

import ast
from importlib.abc import Loader
from importlib.machinery import ModuleSpec
from ideas.ideas_hook import IdeasHook

class IdeasLoader(Loader):
    callback_params: dict[str, Any] | None
    custom_create_module: Callable[..., ModuleType] | None
    exec_: Callable[..., None] | None
    filename: str
    ideas_hook: IdeasHook
    module_class: type[Any]
    parse_source: (
        Callable[[str, str, str], ast.Module]
        | Callable[[ast.Module], ast.Module]
        | None
    )
    source_init: Callable[[], str] | None
    transform_ast: Callable[[ast.AST], ast.AST] | None
    transform_bytecode: Callable[[CodeType], CodeType] | None

    def __init__(
        self,
        filename: str,
        ideas_hook: IdeasHook | None = None,
        callback_params: dict[str, Any] | None = None,
        create_module: Callable[..., ModuleType] | None = None,
        exec_: Callable[..., None] | None = None,
        module_class: type[Any] | None = None,
        source_init: Callable[[], str] | None = None,
        transform_ast: Callable[[ast.AST], ast.AST] | None = None,
        transform_bytecode: Callable[[CodeType], CodeType] | None = None,
        parse_source: (
            Callable[[str, str, str], ast.Module]
            | Callable[[ast.Module], ast.Module]
            | None
        ) = None,
    ) -> None: ...
    def create_module(self, spec: ModuleSpec) -> ModuleType: ...
    def ideas_init_module(self, module: ModuleType) -> ModuleType: ...
    def ideas_get_source(self) -> str: ...
    def ideas_transform_source(self, source: str, module: ModuleType) -> str: ...
    def ideas_parse_source(self, source: str) -> ast.Module: ...
    def ideas_get_bytecode(self, tree: ast.Module) -> CodeType: ...
    def ideas_exec(self, code_object: CodeType, module: ModuleType) -> None: ...
    def exec_module(self, module: ModuleType) -> None: ...
