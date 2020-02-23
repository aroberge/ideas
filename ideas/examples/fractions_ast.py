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
    """Wraps all integers in a call to Integer()"""
    def visit_Num(self, node):
        if isinstance(node.n, int):
            return ast.Call(func=ast.Name(id='Fraction', ctx=ast.Load()),
                            args=[node], keywords=[])
        return node


def transform_ast(tree):
    """Transforms the Abstract Syntax Tree"""
    tree = FractionWrapper().visit(tree)
    ast.fix_missing_locations(tree)
    return tree


new_range = """
old_range = range
def range(n, *args):
    if len(args) == 0:
        return old_range(int(n))
    elif len(args) == 1:
        return old_range(int(n), int(args[0]))
    else:
        return old_range(int(n), int(args[0]), int(args[1]))

"""


def source_init():
    """Adds required imports and function redefinitions"""
    import_fraction = "from fractions import Fraction\n"
    return import_fraction + new_range


def add_hook(verbose_finder=False):
    """Creates and automatically adds the import hook in sys.meta_path"""
    hook = import_hook.create_hook(
        hook_name=__name__,
        source_init=source_init,
        transform_ast=transform_ast,
        verbose_finder=verbose_finder,
    )
    return hook
