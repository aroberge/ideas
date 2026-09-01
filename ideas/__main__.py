"""ideas makes it easy to experiment with alternatives to Python's syntax.

If no source is given, ideas will start an interactive console.
"""

import argparse
from importlib import import_module
import runpy
import sys

import ideas
from ideas import console
from ideas import current_state

transforming_modules = []

parser = argparse.ArgumentParser(
    prog="[-i] -m ideas",
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
    action="append",
    help="""Execute add_hook() from the specified module.
    An attempt is made to import the specified module from the
    usual entries in sys.path; if it not found, it is then
    imported from ideas.examples.""",
    metavar="MODULE",
)

parser.add_argument(
    "--import_",
    action="store_true",
    help="""Imports a module instead of executing it as the __main__ script.
    The extension (.py) must not be included.""",
)

parser.add_argument(
    "-s",
    "--show_changes",
    action="store_true",
    help="""Shows the transformed code before it is executed.""",
)

parser.add_argument(
    "-v",
    "--verbose",
    action="store_true",
    help="""Prints out information about what is being done. Useful for diagnostic.
    Automatically includes --show_changes.""",
)

parser.add_argument(
    "source",
    nargs="?",
    help="""Name of the main Python module (path.to.my_program) to be run as the main script.
    The extension (.py) must not be included.
    """,
)

parser.add_argument(
    "-i", help="""Starts the console after executing a source""", action="store_true"
)


def add_transform(transform):
    """Call the add_hook function for the named module.
    Returns the module object.
    """
    try:
        module = import_module(transform)
    except (ImportError, ModuleNotFoundError):
        pass
    else:
        try:
            add_hook = getattr(module, "add_hook")
        except AttributeError:
            print(f"Module {module} does not contain a function named add_hook")
            return
        add_hook()
        return module

    path = f"ideas.examples.{transform}"
    try:
        module = import_module(path)
    except ImportError:
        print(f"{path} is not a known transformer.")
    else:
        getattr(module, "add_hook")()
        return module


def main() -> None:
    args = parser.parse_args()
    if args.version:
        print(f"\nideas version {ideas.__version__}")
        return

    ideas_does_something = False
    run_as_main = not args.import_

    current_state.show_changes = args.show_changes
    current_state.verbose = args.verbose
    if current_state.verbose:
        current_state.show_changes = True

    if args.add_hook:
        for hook in args.add_hook:
            transforming_modules.append(add_transform(hook))
        ideas_does_something = True

    if not args.source:
        console.start()
        return

    # The command used was something like:
    #     py [...] -m ideas [...] source
    # or
    #     py [...] -m ideas [...] -m or --import_ source
    # All that is left is figuring out how to run the source provided

    current_state.source_argument = args.source
    current_state.run_as_main_argument = run_as_main

    if not ideas_does_something and (sys.flags.interactive or args.i):
        if run_as_main:
            source_dict = runpy.run_module(args.source, run_name="__main__")
        else:
            source_dict = runpy.run_module(args.source)
        console.start(locals_=source_dict)
        return

    if not ideas_does_something:
        print("\n***    `ideas` has been invoked but isn't doing anything.")
        print(f"***    Simply executing `{args.source}` as a main module.\n")
        if run_as_main:
            source_dict = runpy.run_module(args.source, run_name="__main__")
        else:
            source_dict = runpy.run_module(args.source)
        return

    try:
        module = import_module(args.source)
    except ModuleNotFoundError as exc:
        print(f"{exc.__class__.__name__}: {exc.msg}")
        if args.source.endswith(".py"):
            print(
                f"The source argument '{args.source}' must not include the '.py' extension."
            )
            return
        if "." in args.source:
            print(
                f"The source argument '{args.source}' must be a module name without an extension."
            )
            return
        raise

    if sys.flags.interactive or args.i:
        console.start(
            locals_=module.__dict__, transforming_modules=transforming_modules
        )


main()
