from _typeshed import Incomplete

import ast
from importlib.abc import Loader
from importlib.util import decode_source
from ideas import ideas_state
from ideas import utils

class IdeasLoader(Loader):
    callback_params: Incomplete
    custom_create_module: Incomplete
    exec_: Incomplete
    filename: Incomplete
    ideas_hook: Incomplete
    module_class: Incomplete
    parse_source: Incomplete
    source_init: Incomplete
    transform_ast: Incomplete
    transform_bytecode: Incomplete

    def __init__(
        self,
        filename: Incomplete,
        ideas_hook: Incomplete = None,
        callback_params: Incomplete = None,
        create_module: Incomplete = None,
        exec_: Incomplete = None,
        module_class: Incomplete = None,
        source_init: Incomplete = None,
        transform_ast: Incomplete = None,
        transform_bytecode: Incomplete = None,
        parse_source: Incomplete = None,
    ) -> Incomplete: ...
    def create_module(self, spec: Incomplete) -> Incomplete: ...
    def ideas_init_module(self, module: Incomplete) -> Incomplete: ...
    def ideas_get_source(self) -> Incomplete: ...
    def ideas_transform_source(
        self, source: Incomplete, module: Incomplete
    ) -> Incomplete: ...
    def ideas_parse_source(self, source: Incomplete) -> Incomplete: ...
    def ideas_get_bytecode(self, tree: Incomplete) -> Incomplete: ...
    def ideas_exec(self, code_object: Incomplete, module: Incomplete) -> Incomplete: ...
    def exec_module(self, module: Incomplete) -> Incomplete: ...
