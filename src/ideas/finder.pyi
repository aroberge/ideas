from types import ModuleType
from typing import Sequence
from importlib.abc import MetaPathFinder
from importlib.machinery import ModuleSpec
from importlib.util import spec_from_file_location
from ideas.ideas_hook import IdeasHook

def verbose_finder(text: str) -> None: ...

class IdeasMetaPathFinder(MetaPathFinder):
    ideas_hook: IdeasHook
    inform_about_all_possible_paths: bool

    def __init__(self, ideas_hook: IdeasHook) -> None: ...
    def __repr__(self) -> str: ...
    def _set_path(self, path: list[str] | None) -> list[str]: ...
    def find_spec(
        self,
        fullname: str,
        path: Sequence[str] | None,
        target: ModuleType | None = None,
    ) -> ModuleSpec | None: ...
