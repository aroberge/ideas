from _typeshed import Incomplete

import os
import sys
from importlib.abc import MetaPathFinder
from importlib.util import spec_from_file_location
from ideas import ideas_state
from ideas.loader import IdeasLoader
from ideas import utils

def verbose_finder(text: Incomplete) -> Incomplete: ...

class IdeasMetaPathFinder(MetaPathFinder):
    ideas_hook: Incomplete
    inform_about_all_possible_paths: bool

    def __init__(self, ideas_hook: Incomplete) -> Incomplete: ...
    def __repr__(self) -> Incomplete: ...
    def _set_path(self, path: Incomplete) -> Incomplete: ...
    def find_spec(
        self, fullname: Incomplete, path: Incomplete, target: Incomplete = None
    ) -> Incomplete: ...
