"""

Combining transformations
=========================

``experimental_syntax`` is a special module that can be used to combine
transformations. It can be invoked on the command line using::

    python -m ideas -a experimental_syntax

or using something like the following::

    >>> from ideas.examples import experimental_syntax
    >>> experimental_syntax.add_hook()

From that point on, you can add transformations to be applied using
the following normally invalid Python syntax::

    from experimental-syntax import module

Here, ``module`` will be either imported from the current working directory
or from the ``ideas.examples`` subdirectory. After being imported,
the ``module`` is scanned to look for the following functions:

    - ``transform_source``
    - ``transform_ast``
    - ``transform_bytecode``
    - ``ipython_ast_node_transformer``
    - ``source_init``


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


def find_module(module_name):
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
    return module


def add_source_transformer(module):
    """Looks for a function named ``transformed_source`` in ``module``;
    if found, adds it to the list of source transformers.
    """
    if hasattr(module, "transform_source"):
        transform = getattr(module, "transform_source")
        SOURCE_TRANSFORMERS.append(transform)


def add_source_init(module):
    """Looks for a function named ``source_init`` in ``module``;
    if found, returns its content as a string.
    """
    if hasattr(module, "source_init"):
        return getattr(module, "source_init")()
    return ""


def add_ast_transformer(module):
    """Looks for a function named ``transformed_ast`` in ``module``;
    if found, adds it to the list of AST transformers.
    """
    if hasattr(module, "transform_ast"):
        transform = getattr(module, "transform_ast")
        AST_TRANSFORMERS.append(transform)


def add_ipython_ast_node_transformer(module):
    """Determine if it is running in an IPython environment.
    If so, looks for a function named ``ipython_ast_node_transformer``
    in ``module``; if found, adds it to the list of AST transformers
    for IPython.
    """
    if ipython_shell is None:
        return
    if hasattr(module, "ipython_ast_node_transformer"):
        transform = getattr(module, "ipython_ast_node_transformer")
        ipython_shell.ast_transformers.append(transform)


def add_bytecode_transformer(module):
    """Looks for a function named ``transformed_bytecode`` in ``module``;
    if found, adds it to the list of bytecode transformers.
    """
    if hasattr(module, "transform_bytecode"):
        transform = getattr(module, "transform_bytecode")
        BYTECODE_TRANSFORMERS.append(transform)


def identify_experimental_import_statements(source):
    """Identifies if a special import statement of the form

        from experimental-syntax import some_module

    If so, imports the relevant transformers found in that module.
    """
    lines = source.split("\n")
    new_lines = []
    for line in lines:
        match = re.search(IMPORT_STATEMENT, line)
        if match:
            # Remove the invalid syntax statement
            new_lines.append("\n")
            # and scan the module to find the relevant functions.
            module_name = match.group(1).strip()
            module = find_module(module_name)
            if module is None:
                continue
            add_source_transformer(module)
            source_init = add_source_init(module)
            for line in source_init.splitlines():
                new_lines.append(line)
            add_ast_transformer(module)
            add_ipython_ast_node_transformer(module)
            add_bytecode_transformer(module)
        else:
            new_lines.append(line)
    return "\n".join(new_lines)


def transform_source(source, **_kwargs):
    """Applies source transformations."""
    source = identify_experimental_import_statements(source)
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
    """Transform an AST node when running in an IPython environment."""
    for transform in IPYTHON_AST_NODE_TRANSFORMERS:
        try:
            node = transform(node)
        except Exception:
            pass
    return node


def transform_bytecode(byte_code):
    """Applies bytecode transformations."""
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
