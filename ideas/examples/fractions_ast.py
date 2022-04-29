"""
.. admonition:: Summary

    - Demonstrates how to use an import hook that does an AST transformation

Fractional math (AST)
==========================


Consider the following standard Python code::

    >>> x = 1/10
    >>> for i in range(11):
    ...    print(i * x)
    ...
    0.0
    0.1
    0.2
    0.30000000000000004
    0.4
    0.5
    0.6000000000000001
    0.7000000000000001
    0.8
    0.9
    1.0

This is quite surprising for beginners, not familiar with the
limitations of representing floating point numbers.

However, we can "fix" this using an import hook that performs
and Abstract Syntax Tree (AST) transformation::


    > python -m ideas -a fractions_ast
       The following initializing code from ideas is included:

    from fractions import Fraction

    Ideas Console version 0.0.38. [Python version: 3.10.2]

    ideas> x = 1/10

    ideas> for i in range(11):
       ...     print(i * x)
       ...
    0
    1/10
    1/5
    3/10
    2/5
    1/2
    3/5
    7/10
    4/5
    9/10
    1

    ideas> from ideas.session import config

    ideas> config.show_changes = True

    ideas> x = 1/10
    new: x = Fraction(1, 10)

    ideas>
"""
import ast

from ideas import import_hook


class FractionWrapper(ast.NodeTransformer):
    """Wrap all int divisions in a call to Fractions.

    Adapted from https://github.com/diofant/diofant"""

    def visit_BinOp(self, node):
        def is_integer(x):
            if isinstance(x, ast.Num) and isinstance(x.n, int):
                return True
            elif isinstance(x, ast.UnaryOp) and isinstance(x.op, (ast.USub, ast.UAdd)):
                return is_integer(x.operand)
            elif isinstance(x, ast.BinOp) and isinstance(
                x.op, (ast.Add, ast.Sub, ast.Mult, ast.Pow)
            ):
                return is_integer(x.left) and is_integer(x.right)
            else:
                return False

        if isinstance(node.op, ast.Div) and all(
            is_integer(_) for _ in [node.left, node.right]
        ):
            return ast.Call(
                func=ast.Name(id="Fraction", ctx=ast.Load()),
                args=[node.left, node.right],
                keywords=[],
                starargs=None,
                kwargs=None,
            )
        # IPython requires transformations that return a single node
        # whereas ideas works with entire trees.
        try:
            get_python()  # noqa
            return node
        except NameError:
            return self.generic_visit(node)


ipython_ast_node_transformer = FractionWrapper()


def transform_ast(tree, **_kwargs):
    """Transforms the Abstract Syntax Tree or a single node"""
    tree_or_node = FractionWrapper().visit(tree)
    ast.fix_missing_locations(tree_or_node)
    return tree_or_node


def source_init():
    """Adds required import so that ``Fraction`` is a known object."""
    import_fraction = "from fractions import Fraction\n"
    return import_fraction


def add_hook(**_kwargs):
    """Creates and automatically adds the import hook in sys.meta_path"""
    hook = import_hook.create_hook(
        hook_name=__name__,
        source_init=source_init,
        transform_ast=transform_ast,
        ipython_ast_node_transformer=ipython_ast_node_transformer,
    )
    return hook
