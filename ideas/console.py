"""console.py

Adaptation of Python's console found in code.py so that it can be
used with import hooks.
"""

import platform
import os
import sys

from code import InteractiveConsole

from . import __version__


BANNER = "Ideas Console version {}. [Python version: {}]\n".format(
    __version__, platform.python_version()
)
_CONFIG = {}
CONSOLE_NAME = "IdeasConsole"


def configure(**kwargs):
    """Configures various defaults to be used by the console"""
    _CONFIG.update(kwargs)


class IdeasConsole(InteractiveConsole):
    def __init__(
        self,
        locals=None,
        transform_source=None,
        callback_params=None,
        console_dict=None,
    ):
        """This class builds upon Python's code.InteractiveConsole
        so as to work with import hooks.
        """
        self.transform_source = transform_source
        self.callback_params = callback_params

        print(console_dict)

        if console_dict is None:
            console_dict = {}
        if locals is not None:
            console_dict.update(locals)

        super().__init__(locals=console_dict)
        self.filename = CONSOLE_NAME

    def push(self, line):
        """Push a line to the interpreter.

        The line should not have a trailing newline; it may have
        internal newlines.  The line is appended to a buffer and the
        interpreter's runsource() method is called with the
        concatenated contents of the buffer as source.  If this
        indicates that the command was executed or invalid, the buffer
        is reset; otherwise, the command is incomplete, and the buffer
        is left as it was after the line was appended.  The return
        value is True if more input is required, False if the line was dealt
        with in some way (this is the same as runsource()).
        """
        self.buffer.append(line)
        source = "\n".join(self.buffer)

        if self.transform_source is not None:
            source = self.transform_source(
                source, filename=CONSOLE_NAME, callback_params=self.callback_params
            )
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

        The return value is True in case 2, False in the other cases (unless
        an exception is raised).  The return value can be used to
        decide whether to use sys.ps1 or sys.ps2 to prompt the next
        line.
        """
        try:
            code = self.compile(source, filename, symbol)
        except (OverflowError, SyntaxError, ValueError):
            # Case 1
            self.showsyntaxerror(filename)
            return False

        if code is None:
            # Case 2
            return True

        # Case 3
        self.runcode(code)
        return False

    def runcode(self, code):
        """Execute a code object.

        When an exception occurs, friendly_traceback.explain() is called to
        display a traceback.  All exceptions are caught except
        SystemExit, which, unlike the case for the original version in the
        standard library, cleanly exists the program. This is done
        so as to avoid our Friendly-traceback's exception hook to intercept
        it and confuse the users.

        A note about KeyboardInterrupt: this exception may occur
        elsewhere in this code, and may not always be caught.  The
        caller should be prepared to deal with it.
        """
        try:
            exec(code, self.locals)
        except SystemExit:
            os._exit(1)
        except Exception:
            self.showtraceback()


def start(local_vars=None):
    """Starts a console; modified from code.interact"""
    console_defaults = {}

    sys.ps1 = "~>> "

    if local_vars is None:
        local_vars = {}
    else:
        local_vars.update(console_defaults)

    console = IdeasConsole(locals=local_vars, **_CONFIG)

    if _CONFIG:
        print("Configuration values for the console:")
        for key in _CONFIG:
            if _CONFIG[key] is not None:
                print(f"    {key}: {_CONFIG[key]}")
        print("-" * 50)

    console.interact(banner=BANNER)
