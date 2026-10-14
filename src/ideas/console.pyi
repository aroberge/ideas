from _typeshed import Incomplete
from typing import Callable

import ast
import platform
import os
import sys
import traceback
import tokenize
from code import InteractiveConsole
from ideas.__about__ import version
from ideas.session import ideas_state

BANNER: str
_CONFIG: Incomplete
CONSOLE_NAME: str

def configure(
    callback_params: dict | None,
    console_dict: dict | None,
    transform_ast: Callable | None,
    transform_bytecode: Callable | None,
    parse_source: Callable | None,
) -> None: ...

class IdeasConsole(InteractiveConsole):
    callback_params: dict | None
    filename: str
    parse_source: Callable | None
    transform_ast: Callable | None
    transform_bytecode: Incomplete

    def __init__(
        self,
        transform_ast: Callable | None = None,
        transform_bytecode: Callable | None = None,
        callback_params: dict | None = None,
        console_dict: dict | None = None,
        locals_: dict | None = None,
        parse_source: Callable | None = None,
    ) -> None: ...
    def push(self, line: str) -> bool: ...
    def runsource(
        self,
        source: str,
        filename: str = ...,
        symbol: str = "single",
    ) -> bool: ...

def start(
    banner: str = ..., prompt: str = "ideas> ", locals_: dict | None = None
) -> None: ...
