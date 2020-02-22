"""Converts integers literals into instances of the Fraction class.
This works for doing using Python exclusively to do integer arithmetics but it
fails miserably in other contexts that expect ``int``s.
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
    import_fraction = "from fractions import Fraction\n"
    return import_fraction + new_range


def add_hook(verbose_finder=False):
    """Creates and automatically adds the import hook in sys.meta_path"""
    hook = import_hook.create_hook(
        name=__name__,
        source_init=source_init,
        transform_ast=transform_ast,
        verbose_finder=verbose_finder,
    )
    return hook
