from typing import Callable
from _typeshed import Incomplete

from ideas.console import CONSOLE_NAME

shorten_path: Callable[[Incomplete], Incomplete]
CONSTANTS: Incomplete
DECLARED_FINAL: Incomplete

def update_before_console_start(module: Incomplete) -> Incomplete: ...
def make_class(on_prevent_change_feedback: Incomplete = True) -> Incomplete: ...

class FinalDict(dict):  # type: ignore
    __file__: Incomplete
    on_prevent_change_feedback: Incomplete

    def __init__(
        self, module_filename: Incomplete, on_prevent_change_feedback: Incomplete = True
    ) -> None: ...
    def __setitem__(self, key: Incomplete, value: Incomplete) -> Incomplete: ...
    def __delitem__(self, key: Incomplete) -> Incomplete: ...
    def setdefault(self, key: Incomplete, default: Incomplete = None) -> Incomplete: ...

def transform_source(
    source: Incomplete, filename: Incomplete = None, **_kwargs: Incomplete
) -> Incomplete: ...
def exec_(
    code_object: Incomplete,
    filename: Incomplete = None,
    module: Incomplete = None,
    callback_params: Incomplete = None,
    **kwargs: Incomplete,
) -> Incomplete: ...
def on_change_print(
    filename: str = "",
    key: Incomplete = None,
    value: Incomplete = None,
    kind: Incomplete = None,
    in_final: Incomplete = False,
) -> Incomplete: ...
def add_hook(
    on_prevent_change_feedback: Incomplete = None, **_kwargs: Incomplete
) -> Incomplete: ...
