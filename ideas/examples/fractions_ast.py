"""fractions_ast.py
----------------

Converts integers literals into instances of the Fraction class at the
Abstract Syntax Tree level.
This works for doing using Python exclusively to do integer arithmetics but it
fails miserably in other contexts that expect ``int``.

It is only meant as a demo of AST transformations.
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
        try:
            get_python()  # noqa
            return node
        except NameError:
            return self.generic_visit(node)


def transform_ast(tree, **_kwargs):
    """Transforms the Abstract Syntax Tree"""
    tree = FractionWrapper().visit(tree)
    ast.fix_missing_locations(tree)
    return tree


def source_init():
    """Adds required imports"""
    import_fraction = "from fractions import Fraction\n"
    return import_fraction


def add_hook(**_kwargs):
    """Creates and automatically adds the import hook in sys.meta_path"""
    hook = import_hook.create_hook(
        hook_name=__name__,
        source_init=source_init,
        transform_ast=transform_ast,
        ipython_ast_node_transformer=FractionWrapper(),
    )
    return hook
