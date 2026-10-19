from typing import Callable, Any

from code import InteractiveConsole
from types import CodeType
import ast

BANNER: str
_CONFIG: dict[str, Any]
CONSOLE_NAME: str

def configure(
    callback_params: dict[str, Any] | None,
    console_dict: dict[str, Any] | None,
    transform_ast: Callable[[ast.AST], ast.AST] | None,
    transform_bytecode: Callable[[CodeType], CodeType] | None,
    parse_source: (
        Callable[[str, str, str], ast.Module]
        | Callable[[ast.Module], ast.Module]
        | None
    ),
) -> None: ...

class IdeasConsole(InteractiveConsole):
    callback_params: dict[str, Any] | None
    filename: str
    parse_source: Callable[[str], str] | None
    transform_ast: Callable[[ast.AST], ast.AST] | None
    transform_bytecode: Callable[[CodeType], CodeType] | None

    def __init__(
        self,
        transform_ast: Callable[[ast.AST], ast.AST] | None = None,
        transform_bytecode: Callable[[CodeType], CodeType] | None = None,
        callback_params: dict[str, Any] | None = None,
        console_dict: dict[str, Any] | None = None,
        locals_: dict[str, Any] | None = None,
        parse_source: (
            Callable[[str, str, str], ast.Module]
            | Callable[[ast.Module], ast.Module]
            | None
        ) = None,
    ) -> None: ...
    def push(self, line: str) -> bool: ...
    def runsource(
        self,
        source: str,
        filename: str = ...,
        symbol: str = "single",
    ) -> bool: ...

def start(
    banner: str = ..., prompt: str = "ideas> ", locals_: dict[str, Any] | None = None
) -> None: ...
