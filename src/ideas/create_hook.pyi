from typing import Callable, Sequence, Any
import ast
from ideas import utils
from ideas.ideas_hook import IdeasHook
from types import CodeType, ModuleType

def create_hook(
    name: str = "",
    callback_params: dict[str, Any] | None = None,
    console_only: bool = False,
    create_module: Callable[..., ModuleType] | None = None,
    does_not_play_well_with_others: bool = False,
    excluded_paths: list[str] | type[utils.DEFAULT] | None = utils.DEFAULT,
    exec_: Callable[..., None] | None = None,
    extensions: Sequence[str] | list[str] | None = None,
    parse_source: (
        Callable[[str, str, str], ast.Module]
        | Callable[[ast.Module], ast.Module]
        | None
    ) = None,
    source_init: Callable[[], str] | None = None,
    transform_ast: Callable[[ast.AST], ast.AST] | None = None,
    transform_bytecode: Callable[[CodeType], CodeType] | None = None,
    transform_source: Callable[[str], str] | None = None,
) -> IdeasHook | None: ...
