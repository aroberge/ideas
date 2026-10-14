from _typeshed import Incomplete

import argparse
from importlib import import_module
from ideas import console
from ideas import ideas_state
from ideas import transform

class ParseKwargs(argparse.Action):
    def __call__(
        self,
        parser: Incomplete,
        namespace: Incomplete,
        values: Incomplete,
        option_string: Incomplete = None,
    ) -> Incomplete: ...

parser: argparse.ArgumentParser

def add_transform(
    transform: Incomplete, callback_params: Incomplete = ...
) -> Incomplete: ...
def main() -> None: ...
