from typing import Literal
from _typeshed import Incomplete

import ast
from ideas import create_hook

DELIMITERS: tuple[Literal["__pythonji__"], Literal["__"]]

def transform_source(source: Incomplete, **_kwargs: Incomplete) -> Incomplete: ...

class EmojiTransformer(ast.NodeTransformer):
    def visit_Str(self, node: Incomplete) -> Incomplete: ...

def transform_ast(tree: Incomplete, **_kwargs: Incomplete) -> Incomplete: ...
def add_hook(**_kwargs: Incomplete) -> Incomplete: ...
