"""Enabling emojis as normal characters"""
import ast
import sys

try:
    import emoji  # noqa
except ModuleNotFoundError:
    print("You need to install 'emoji' from pypi.")
    sys.exit()

from ideas import import_hook


DELIMITERS = ("__pythonji__", "__")


def transform_source(source, **_kwargs):
    return emoji.demojize(source, delimiters=DELIMITERS)


class EmojiTransformer(ast.NodeTransformer):
    def visit_Str(self, node):
        return ast.copy_location(
            ast.Str(s=emoji.emojize(node.s, delimiters=DELIMITERS)), node
        )


def transform_ast(tree, **_kwargs):
    """Transforms the Abstract Syntax Tree or a single node"""
    tree_or_node = EmojiTransformer().visit(tree)
    ast.fix_missing_locations(tree_or_node)
    return tree_or_node


def add_hook(**_kwargs):
    """Creates and adds the import hook in sys.meta_path.
    Uses a custom extension for the exception hook."""
    hook = import_hook.create_hook(
        transform_source=transform_source,
        transform_ast=transform_ast,
        hook_name=__name__,
        extensions=[".🐍"],
    )
    return hook
