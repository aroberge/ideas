from _typeshed import Incomplete

import sys
import traceback
from ideas.ideas_hook import IdeasHook

class State:
    _codecs_search_functions: Incomplete
    _custom_codecs_source_transform: Incomplete
    _hooks: Incomplete
    _patches: Incomplete
    active_console: bool
    console_name: str
    full_traceback: bool
    last_exception: Incomplete
    max_nb_lines: int
    original_source: str
    run_as_main_argument: bool
    show_changes: bool
    show_original: bool
    source_argument: Incomplete
    source_inits: Incomplete
    verbose: bool
    verbose_finder: bool
    verbose_loader: bool

    def __init__(self) -> Incomplete: ...
    def _clear(self) -> Incomplete: ...
    def help(self) -> Incomplete: ...
    def get_hook_by_name(self, name: Incomplete) -> Incomplete: ...
    def _add_hook(self, hook: Incomplete) -> Incomplete: ...
    def remove_hook(self, name_or_hook: Incomplete) -> Incomplete: ...
    def list_hooks(self) -> Incomplete: ...
    def disable_hook(self, name_or_hook: Incomplete) -> Incomplete: ...
    def enable_hook(self, name_or_hook: Incomplete) -> Incomplete: ...
    def _print_transformed(
        self, source: Incomplete, header: Incomplete = "New"
    ) -> Incomplete: ...
    def print_source(
        self, source: Incomplete, header: Incomplete = "Original/New"
    ) -> Incomplete: ...
    def source_transforms(
        self,
        source: Incomplete,
        filename: Incomplete = None,
        module: Incomplete = None,
        callback_params: Incomplete = None,
        console_dict: Incomplete = None,
        **kwargs: Incomplete,
    ) -> Incomplete: ...
    def add_patch(self, module_name: Incomplete, func: Incomplete) -> Incomplete: ...
    def remove_patches(self) -> Incomplete: ...
    def exception_hook(
        self, exc_type: Incomplete, exc_value: Incomplete, tb: Incomplete
    ) -> Incomplete: ...

ideas_state: State
