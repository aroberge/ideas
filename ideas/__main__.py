"""ideas makes it easy to experiment with alternatives to Python's syntax.

If no source is given, ideas will start an interactive console.
"""

import argparse
from importlib import import_module
import sys

import ideas
from ideas import console
from ideas.session import config


parser = argparse.ArgumentParser(
    formatter_class=argparse.RawDescriptionHelpFormatter,
    description=__doc__,
)

parser.add_argument(
    "-v",
    "--version",
    help="Only displays the current version.",
    action="store_true",
)

parser.add_argument(
    "-a",
    "--add_hook",
    nargs=1,
    help="""Execute add_hook() from the specified module.
    An attempt is made to import the specified module from the
    usual entries in sys.path; if it not found, it is then
    imported from ideas.examples.""",
    metavar="MODULE",
)

parser.add_argument(
    "-r",
    "--register_codec",
    nargs=1,
    help="""Execute the named module to register a codec. The specified module
    is either found in the current directory or, if not found,
    from ideas.examples.""",
    metavar="MODULE",
)

parser.add_argument(
    "-s",
    "--show_changes",
    action="store_true",
    help="""Shows the transformed code before it is executed.""",
)

parser.add_argument(
    "source",
    nargs="?",
    help="""Name of the main Python module (path.to.my_program) to be imported.
    """,
)


def add_transform(transform):
    """Call the add_hook function for the named module."""
    try:
        module = import_module(transform)
    except (ImportError, ModuleNotFoundError):
        pass
    else:
        try:
            getattr(module, "add_hook")()
        except AttributeError:
            print(f"Module {module} does not contain a function named add_hook")
            return

    path = f"ideas.examples.{transform}"
    try:
        module = import_module(path)
    except ImportError:
        print(f"{path} is not a known transformer.")
    else:
        getattr(module, "add_hook")()


def register_codec(encoding):
    """Executes a module that is expected to register a custom encoding."""
    try:
        import_module(encoding)
    except (ImportError, ModuleNotFoundError):
        pass

    path = f"ideas.examples.{encoding}"
    try:
        import_module(path)
    except ImportError:
        print(f"{path} is not a known codec.")


def main() -> None:
    args = parser.parse_args()
    if args.version:
        print(f"\nideas version {ideas.__version__}")
        return

    config.show_changes = bool(args.show_changes)

    if args.add_hook and args.register_codec:
        print("You can only use one option at a time:")
        print("- either use a source transformation with -a (--add_hook); or")
        print("- register a custom codec with -r (--register_codec),")
        return

    if args.add_hook:
        add_transform(args.add_hook[0])
    if args.register_codec:
        register_codec(args.register_codec[0])

    if args.source is not None:
        if args.source.endswith(".py"):
            args.source = args.source[:-3]
        module = import_module(args.source)
        if sys.flags.interactive:
            console.start(locals=module.__dict__, prompt=">>> ")
    else:
        console.start(prompt=">>> ")


main()
