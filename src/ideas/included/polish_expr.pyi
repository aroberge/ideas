from _typeshed import Incomplete

import ast
from ast import (
    Add,
    Assign,
    BinOp,
    Constant,
    Div,
    Expr,
    Interactive,
    Module,
    Mult,
    Name,
    Sub,
    fix_missing_locations,
    literal_eval,
)
import token
import token_utils
from typing import Iterable
from ideas import create_hook

class Parser:
    filename: str
    lasttok: None
    nexttok: Token
    tokengen: Generator[Token]

    def __init__(
        self, tokens: Iterable[token_utils.Token], filename: str
    ) -> Incomplete: ...
    def advance(self) -> Incomplete: ...
    def peekmatch(
        self, toktype: Incomplete, string: Incomplete = None
    ) -> Incomplete: ...
    def match(self, toktype: Incomplete, string: Incomplete = None) -> Incomplete: ...
    def expect(self, toktype: Incomplete, string: Incomplete = None) -> Incomplete: ...
    def _syntaxerror(self, msg: Incomplete, tok: Incomplete = None) -> Incomplete: ...
    def file(self) -> ast.Module: ...
    def interactive(self) -> ast.Interactive: ...
    def eval(self) -> ast.expr: ...
    def stmt(self, name: Incomplete = None) -> ast.stmt: ...
    def expr(self) -> ast.expr: ...

def parse_source(
    src: Incomplete, filename: Incomplete, mode: Incomplete, **_kwargs: Incomplete
) -> Incomplete: ...
def add_hook(**_kwargs: Incomplete) -> Incomplete: ...
