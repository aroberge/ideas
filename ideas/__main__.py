"""ideas makes it easy to experiment to experiment
with alternatives to Python's syntax.

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
    "--version",
    help="Only displays the current version.",
    action="store_true",
)


parser.add_argument(
    "-a",
    "--add_hook",
    nargs=1,
    help="""Execute add_hook() from module ADD_HOOK. The specified module
    is either found in the current directory or, if not found,
    from ideas.examples.""",
)

parser.add_argument(
    "-v",
    "--verbose",
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
    try:
        module = import_module(transform)
    except (ImportError, ModuleNotFoundError):
        pass
    else:
        try:
            getattr(module, "add_hook")()
        except AttributeError:
            print(f"Module {transform} does not contain a function named add_hook")
            return

    path = f"ideas.examples.{transform}"
    try:
        module = import_module(path)
    except ImportError:
        print(f"{path} is not a known transformer.")
    else:
        getattr(module, "add_hook")()


def main() -> None:
    args = parser.parse_args()
    if args.version:  # pragma: no cover
        print(f"\nideas version {ideas.__version__}")
        sys.exit()

    config.show_transformed = bool(args.verbose)

    if args.add_hook:
        add_transform(args.add_hook[0])

    if args.source is not None:
        if args.source.endswith(".py"):
            args.source = args.source[:-3]
        module = import_module(args.source)
        if sys.flags.interactive:  # pragma: no cover
            console.start(locals=module.__dict__, prompt=">>> ")
    else:
        console.start(prompt=">>> ")


main()
