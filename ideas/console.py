"""console.py
--------------

Adaptation of Python's console found in code.py so that it can be
used with import hooks.
"""

import ast
import platform
import readline
import os
import sys
import traceback
import tokenize

from code import InteractiveConsole

from . import __version__
from .session import config


BANNER = (
    f"Ideas Console version {__version__}. "
    + f"[Python version: {platform.python_version()}]"
)
_CONFIG = {}
CONSOLE_NAME = config.console_name


def configure(**kwargs):
    """Configures various defaults to be used by the console"""
    _CONFIG.update(kwargs)


class IdeasConsole(InteractiveConsole):
    """An interactive console that works with source transformations,
    AST transformations and Bytecode transformations.

    It should not need to be instantiated directly.
    """

    def __init__(  # pylint: disable=R0913
        self,
        source_init=None,
        transform_ast=None,
        transform_bytecode=None,
        transform_source=None,
        callback_params=None,
        console_dict=None,
        locals_=None,
        parse_source=None,
    ):
        """This class builds upon Python's code.InteractiveConsole
        to work with import hooks.
        """
        self.transform_ast = transform_ast
        self.transform_bytecode = transform_bytecode
        self.transform_source = transform_source
        self.parse_source = parse_source
        self.callback_params = callback_params

        # console_dict can be a custom dict-like object.
        # See ideas.examples.constants.py for an example.
        if console_dict is None:
            console_dict = {}
        if locals_ is not None:
            console_dict.update(**locals_)

        readline.parse_and_bind('tab: complete')

        super().__init__(locals=console_dict)
        self.filename = CONSOLE_NAME

        if source_init is not None:
            try:
                exec(source_init(), self.locals)  # pylint: disable=W0122
            except Exception:  # pylint: disable=W0703
                self.showtraceback()
            else:
                print("   The following initializing code from ideas is included:\n")
                print(source_init())

    def push(self, line):
        """Push a line to the interpreter.

        The line should not have a trailing newline; it may have
        internal newlines.  The line is appended to a buffer and the
        interpreter's runsource() method is called with the
        concatenated contents of the buffer as the source.  If this
        indicates that the command was executed or invalid, the buffer
        is reset; otherwise, the command is incomplete, and the buffer
        is left as it was after the line was appended.  The return
        value is True if more input is required, False if the line was dealt
        with in some way (this is the same as runsource()).
        """
        self.buffer.append(line)
        source = "\n".join(self.buffer)
        config.original = source

        if self.transform_source is not None:
            last_line = source.endswith("\n")  # signals the end of a block
            try:
                source = self.transform_source(
                    source, filename=CONSOLE_NAME, callback_params=self.callback_params
                )
            except tokenize.TokenError:
                # Pass on the original source so that open (, or additional)
                # can be handled correctly as either SyntaxErrors or indication
                # that more code is needed.
                more = self.runsource(source, CONSOLE_NAME)
                if not more:
                    self.resetbuffer()
                return more
            except Exception as exc:
                print("Error when executing transform_source:")
                print("   ", traceback.format_exception_only(type(exc), exc)[0].strip())
                self.resetbuffer()
                return
            # Some transformations may add some extra "\n" (usually at most one)
            if not last_line:
                source = source.rstrip("\n")
        more = self.runsource(source, CONSOLE_NAME)
        if not more:
            self.resetbuffer()
        return more

    def runsource(self, source, filename=CONSOLE_NAME, symbol="single"):
        """Compile and run some source in the interpreter.

        Arguments are as for compile_command().

        One several things can happen:

        1) The input is incorrect; compile_command() raised an
        exception (SyntaxError or OverflowError).  A syntax traceback
        will be printed .

        2) The input is incomplete, and more input is required;
        compile_command() returned None.  Nothing happens.

        3) The input is complete; compile_command() returned a code
        object.  The code is executed by calling self.runcode() (which
        also handles run-time exceptions, except for SystemExit).
        However, if an AST transformation is performed, we go back
        to the source and recompile in two steps so that we can
        perform an AST transformation.

        The return value is True in case 2, False in the other cases (unless
        an exception is raised).  The return value can be used to
        decide whether to use sys.ps1 or sys.ps2 to prompt the next
        line.
        """
        try:
            if self.parse_source is not None:
                tree = self.parse_source(source, filename, symbol)
                code_obj = tree and compile(tree, filename, symbol)
            else:
                code_obj = self.compile(source, filename, symbol)
        except (OverflowError, SyntaxError, ValueError):
            # Case 1
            config.print_transformed(source)
            self.showsyntaxerror(filename)
            return False

        if code_obj is None:
            # Case 2
            return True
        config.print_transformed(source)
        # Case 3

        if self.transform_ast is not None:
            # recreate code object, this time, with ast transform
            tree = ast.parse(source, filename)
            tree = self.transform_ast(tree)
            if hasattr(ast, "unparse"):
                try:
                    source = ast.unparse(tree)
                    config.print_transformed(source)
                    source += "\n"
                except RecursionError:
                    if config.show_changes:
                        print(
                            "Warning: cannot unparse the code sample to show changes."
                        )
                    code_obj = compile(tree, filename, "exec")
                except Exception as e:
                    print("Error when executing transform_ast:")
                    print("   ", traceback.format_exception_only(type(e), e)[0].strip())
                    return False
                else:
                    code_obj = self.compile(source, filename, symbol)
            else:
                code_obj = compile(tree, filename, "exec")
            if code_obj is None:
                return True

        if self.transform_bytecode is not None:
            try:
                code_obj = self.transform_bytecode(code_obj)
            except Exception as e:
                print("Error when executing transform_bytecode:")
                print("   ", traceback.format_exception_only(type(e), e)[0].strip())
                return False

        try:
            self.runcode(code_obj)
        except SystemExit:
            os._exit(0)
        return False


def start(banner=BANNER, prompt="ideas> ", locals_=None):
    """Starts a special console that works with import hooks."""
    if len(prompt) >= 4:
        sys.ps2 = (len(prompt) - 4) * " " + "... "
    sys.ps1 = "\n" + prompt
    if locals_ is None:
        locals_ = {"config": config}
    elif "Ideas" in locals_:
        if "ideas_config" in locals_:
            print("Ideas' configuration object is not available.")
        else:
            print("Ideas' configuration object is available as ideas_config")
            locals_["ideas_config"] = config
    else:
        locals_["config"] = config
    console = IdeasConsole(**_CONFIG, locals_=locals_)

    if console.transform_ast is not None and not hasattr(ast, "unparse"):
        banner += """
    AST transformations applied: you will need to explicitly
    call print() to see the result of a command since ast.unparse
    does not exist in your Python version.
    """
    console.interact(banner=banner)
