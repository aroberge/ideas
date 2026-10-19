from _typeshed import Incomplete
from typing import Sequence, Any
from types import ModuleType

import argparse
from importlib import import_module

class ParseKwargs(argparse.Action):
    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: Any,
        values: str | Sequence[Any] | None,
        option_string: str | None = None,
    ) -> None: ...

parser: argparse.ArgumentParser

def add_transform(
    transform: str, callback_params: dict[str, Any] = ...
) -> ModuleType: ...
def main() -> None: ...
