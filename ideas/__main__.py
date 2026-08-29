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
    "-m",
    "--run_as_main",
    action="store_true",
    help="""Name of the main Python module (path.to.my_program) to be executed as a main scrit.
    The extension (.py) must not be included.""",
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
    "-v",
    "--verbose",
    action="store_true",
    help="""Prints out information about what is being done. Useful for diagnostic.
    Automatically includes --show_changes.""",
)

parser.add_argument(
    "source",
    nargs="?",
    help="""Name of the main Python module (path.to.my_program) to be imported.
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
    ideas_does_something = False
    args = parser.parse_args()
    if args.version:
        print(f"\nideas version {ideas.__version__}")
        return

    current_state.show_changes = bool(args.show_changes)
    current_state.verbose = bool(args.verbose)
    if current_state.verbose:
        current_state.show_changes = True

    if args.add_hook and args.register_codec:
        print("From the command line, you can only use one option at a time:")
        print("- Either use one or more source transformations")
        print("  with each transformation preceded by the -a (--add_hook) flag; or\n")
        print("- Register a custom codec with -r (--register_codec),")
        return

    if args.add_hook:
        for hook in args.add_hook:
            transforming_modules.append(add_transform(hook))
        ideas_does_something = True

    if args.register_codec:
        register_codec(args.register_codec[0])
        ideas_does_something = True

    if args.source is None:
        console.start()
        return

    # The command used was something like:
    #     py [...] -m ideas [...] source
    # All that is left is figuring out how to run the source provided
    # which is meant to be the module __main__ instead of `ideas` itself

    if not ideas_does_something and (sys.flags.interactive or args.i):
        if args.run_as_main:
            source_dict = runpy.run_module(args.source, run_name="__main__")
        else:
            source_dict = runpy.run_module(args.source)
        console.start(locals_=source_dict)
        return

    if not ideas_does_something:
        print("\n***    `ideas` has been invoked but isn't doing anything.")
        print(f"***    Simply executing `{args.source}` as a main module.\n")
        if args.run_as_main:
            source_dict = runpy.run_module(args.source, run_name="__main__")
        else:
            source_dict = runpy.run_module(args.source)
        return

    if args.run_as_main:
        current_state.source_argument = args.source
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
    finally:
        current_state.source_argument = None

    if sys.flags.interactive or args.i:
        console.start(
            locals_=module.__dict__, transforming_modules=transforming_modules
        )


main()
