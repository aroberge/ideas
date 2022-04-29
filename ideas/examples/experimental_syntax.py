"""
Special module to combine transformations.

A transformer (source, AST, or bytecode) can be added using the syntax::

    from experimental-syntax import module
"""
import ast
from importlib import import_module
import re

from ideas import import_hook

IMPORT_STATEMENT = re.compile("from experimental-syntax import (.*)")
SOURCE_TRANSFORMERS = []
AST_TRANSFORMERS = []
BYTECODE_TRANSFORMERS = []
IPYTHON_AST_NODE_TRANSFORMERS = []

try:
    ipython_shell = get_ipython()  # noqa
except NameError:
    ipython_shell = None


def add_source_transformer(module_name):
    # First, try to import from current working directory
    try:
        module = import_module(module_name)
    except (ImportError, ModuleNotFoundError):
        path = f"ideas.examples.{module_name}"
        try:
            module = import_module(path)
        except ImportError:
            print(f"{module_name} is not a known module.")
            return None
        else:
            module_name = path

    if hasattr(module, "transform_source"):
        transform = getattr(module, "transform_source")
        SOURCE_TRANSFORMERS.append(transform)
    return module


def add_source_init(module):
    if hasattr(module, "source_init"):
        return getattr(module, "source_init")()
    return ""


def add_ast_transformer(module):
    if hasattr(module, "transform_ast"):
        transform = getattr(module, "transform_ast")
        AST_TRANSFORMERS.append(transform)


def add_ipython_ast_node_transformer(module):
    if ipython_shell is None:
        return
    if hasattr(module, "ipython_ast_node_transformer"):
        transform = getattr(module, "ipython_ast_node_transformer")
        ipython_shell.ast_transformers.append(transform)


def add_bytecode_transformer(module):
    if hasattr(module, "transform_bytecode"):
        transform = getattr(module, "transform_bytecode")
        BYTECODE_TRANSFORMERS.append(transform)


def transform_source(source, **_kwargs):
    lines = source.split("\n")
    new_lines = []
    for line in lines:
        match = re.search(IMPORT_STATEMENT, line)
        if match:
            module_name = match.group(1).strip()
            module = add_source_transformer(module_name)
            source_init = add_source_init(module)
            for line in source_init.splitlines():
                new_lines.append(line)
            # Ensure that there is a line to process for IPython
            new_lines.append("\n")
            add_ast_transformer(module)
            add_ipython_ast_node_transformer(module)
            add_bytecode_transformer(module)
        else:
            new_lines.append(line)
    source = "\n".join(new_lines)

    for transform in SOURCE_TRANSFORMERS:
        source = transform(source)

    return source


def transform_ast(tree, **_kwargs):
    """Transforms the Abstract Syntax Tree"""
    for transform in AST_TRANSFORMERS:
        tree = transform(tree)
        ast.fix_missing_locations(tree)
    return tree


def ipython_ast_node_transformer(node):
    for transform in IPYTHON_AST_NODE_TRANSFORMERS:
        try:
            node = transform(node)
        except Exception:
            pass
    return node


def transform_bytecode(byte_code):
    for transform in BYTECODE_TRANSFORMERS:
        byte_code = transform(byte_code)
    return byte_code


def add_hook(**_kwargs):
    """Creates and adds the import hook in sys.meta_path.
    Uses a custom extension for the exception hook."""
    hook = import_hook.create_hook(
        transform_source=transform_source,
        transform_ast=transform_ast,
        transform_bytecode=transform_bytecode,
        hook_name=__name__,
    )
    return hook
