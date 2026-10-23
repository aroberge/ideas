from typing import Callable, Any
from types import ModuleType, TracebackType
import codecs

from ideas.ideas_hook import IdeasHook

class State:
    _codecs_search_functions: dict[str, Callable[[str], codecs.CodecInfo]]
    _custom_codecs_source_transform: Callable[[str], str]
    _hooks: list[IdeasHook]
    _patches: dict[str, list[Any]]
    active_console: bool
    console_name: str
    full_traceback: bool
    last_exception: BaseException | None
    max_nb_lines: int
    original_source: str
    run_as_main_argument: bool
    show_changes: bool
    show_original: bool
    source_argument: str | None
    source_inits: list[Callable[[], Any]]
    verbose: bool
    verbose_finder: bool
    verbose_loader: bool

    def __init__(self) -> None: ...
    def _clear(self) -> None: ...
    def help(self) -> None: ...
    def get_hook_by_name(self, name: str) -> IdeasHook | None: ...
    def _add_hook(self, hook: IdeasHook) -> None: ...
    def remove_hook(self, name_or_hook: str | IdeasHook) -> None: ...
    def list_hooks(self) -> None: ...
    def disable_hook(self, name_or_hook: str | IdeasHook) -> None: ...
    def enable_hook(self, name_or_hook: str | IdeasHook) -> None: ...
    def _print_transformed(self, source: str, header: str = "New") -> None: ...
    def print_source(self, source: str, header: str = "Original/New") -> None: ...
    def source_transforms(
        self,
        source: str,
        filename: str | None = None,
        module: ModuleType | None = None,
        callback_params: dict[str, Any] | None = None,
        console_dict: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> str: ...
    def add_patch(self, module_name: str, func: Callable[..., None]) -> None: ...
    def remove_patches(self) -> None: ...
    def exception_hook(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        tb: TracebackType | None,
    ) -> None: ...

ideas_state: State
