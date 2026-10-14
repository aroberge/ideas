from _typeshed import Incomplete

import ast
import sys
from ideas import create_hook
from ideas import utils

class FractionWrapper(ast.NodeTransformer):
    def visit_BinOp(self, node: Incomplete) -> Incomplete: ...

ipython_ast_node_transformer: FractionWrapper

def transform_ast(tree: Incomplete, **_kwargs: Incomplete) -> Incomplete: ...
def source_init() -> Incomplete: ...
def add_hook(**_kwargs: Incomplete) -> Incomplete: ...
