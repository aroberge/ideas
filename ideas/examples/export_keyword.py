"""
Export as a soft keyword
========================

This import hook was **inspired** by
`PEP 842 (withdrawn) <https://peps.python.org/pep-0842/>`_
which suggested the addition of ``export`` as a soft keyword
to be used in the following three cases::

    export identifier = ...
    export def function_name(): ...
    export class ClassName(): ...


.. sidebar:: Competing PEP

   We note that `PEP 844 <https://peps.python.org/pep-0844/>`_
   propose the inclusion of functions defined in the
   ``at_public`` project as Python builtins with a 
   similar goal, i.e. automatically updating ``__all__``
   while enabling people reading the source code to
   easily identify which names are meant to be public.

   We do acknowledge that adding a builtin rather than
   introducing a new syntax, would be much less disruptive,
   and much easier to adopt overall.
   
The result of using this soft keyword is to automatically 
add the name of the object to ``__all__``.

An additional option that we included, also inspired by
PEP 842, is the possibility to automatically define a custom
``__dir__`` which would result in only the "exported"
identifiers to be visible within an REPL.

This import hook complements well and can easily be combined 
the pep_843 import hook described in a previous section.

.. important::

    The goal of **ideas** is to offer the possibility to
    easily experiment with alternatives
    to Python's normal syntax, exploring various "what if"
    scenarios.

    Unusually for this project, since two related examples
    are inspired by actual proposed PEPs, we give a
    **highly subjective** evaluation of what the proposed
    syntax would achieve.

Combining the import hooks export_keyword and pep_843
would result in the following:

    1. Reduce the work required in creating a public interface
       by adding names to ``__all__`` by hand while reducing
       the possibility of errors.
    2. Enabling anyone reading source code to easily identify
       which names are meant to be part of the public
       interface.
    3. Enable developers to easily change names in their
       various subdirectories while maintaining a stable
       public API.
    4. With the inclusion of a an optional custom ``__dir__``
       as described below, enable programmers to use a REPL
       to explore the various files of a project and, know
       which names can likely be safely used as they have
       been declared to be "public" via an ``export``
       statement.


First example: export keyword only
-----------------------------------

Consider the following case::

    # sample_file.py

    from math import pi

    export PI = pi

    export public = "public variable"

    export def useful_fn():
        print("This is a very useful function")

    def private():
        print("I want to be able to change my name.")

    secret = "Ideas's code is a mess."

We will import and explore the content of this file in two
different sessions. First, with the default Python ``dir``.

.. code-block::

    >>> from ideas.examples.export_keyword import add_hook
    >>> hook = add_hook()
    >>> # Let's first see what's already here
    >>> dir()
    ['__annotations__', '__builtins__', '__doc__', '__loader__', '__name__', '__package__', '__spec__', 'add_hook', 'hook']
    >>> __name__
    '__main__'
    >>> # Let's import a sample file
    >>> import sample_file
    >>> dir(sample_file)
    ['PI', '__all__', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'pi', 'private', 'public', 'secret', 'useful_fn']
    >>> sample_file.__name__
    'sample_file'
    >>> # We see many names; let's import "everything"
    >>> from sample_file import *
    >>> dir()
    ['PI', '__annotations__', '__builtins__', '__doc__', '__loader__', '__name__', '__package__', '__spec__', 'add_hook', 'hook', 'public', 'sample_file', 'useful_fn']
    >>> # We did not import pi, private and secret. Did anything else change?
    >>> __name__
    '__main__'
    >>> # Python does the right thing when it comes to dunders ...

Let's try again, using the ``public_dir`` option.

.. code-block::

    >>> from ideas.examples.export_keyword import add_hook
    >>> hook = add_hook(public_dir=True)  # optional argument
    >>> import sample_file
    >>> dir(sample_file)
    ['PI', 'public', 'useful_fn']
    >>> # much cleaner; let's import everything
    >>> from sample_file import *
    >>> dir()
    ['PI', '__annotations__', '__builtins__', '__doc__', '__loader__', '__name__', '__package__', '__spec__', 'add_hook', 'hook', 'public', 'sample_file', 'useful_fn']
    >>> sample_file.secret
    "Ideas's code is a mess."
    >>> # Even though it was hidden, the secret is not safe if you are determined enough



.. warning::

    Do not use continuation characters in your sample code.
    The current transformation might not handle them correctly.

"""

from ideas.utils import get_significant_tokens
import token_utils
from ideas import current_state

# A better programmer would likely have written a recursive descent parser,
# or something similar, to process the source, extract the relevant information
# to make the appropriate change.
#
# what I did instead is to proceed in two parts, going through the entire source once
# and extracting the relevant information, before going through the entire source
# a second time to make the appropriate changes.
#
# When I have more time, I plan to add comments below to explain
# the reasoning behind this code.


class ExportInfo:
    def __init__(self, source):
        self.source = source
        self.export_statements_info = []
        self.indentation = 0
        self.current_row = -1
        self.inside_class_or_def = []
        self.open_brackets = []  # Any ([{ open but not closed
        self.class_or_def_indent = -1
        self.prev_token = None
        self.reset_flags()

    def reset_flags(self):
        self.begin_export = False
        self.export_class_or_def_name = False
        self.export_variable = False
        self.export_stmt_info = {}

    def get_info(self):
        for self.token in get_significant_tokens(self.source):

            if not self.begin_export:
                if self.skip_over_irrelevant_token():
                    self.prev_token = self.token
                    continue

            if self.token.start_row > self.current_row and self.token == "export":
                self.init_export_statement()
                self.current_row = self.token.start_row
                self.prev_token = self.token
                continue

            # Restrict "export identifier ... = " to be on a single line.
            if self.token.start_row > self.current_row:
                self.begin_new_statement()
                self.prev_token = self.token
                continue

            if not self.begin_export:
                self.prev_token = self.token
                continue

            self.process_until_name_found()
            self.prev_token = self.token

        return self.export_statements_info

    def skip_over_irrelevant_token(self):
        if self.token.string in "([{":
            self.open_brackets.append(self.token.string)
            return True
        elif self.token.string in ")]}":
            self.open_brackets.pop()
            return True
        elif self.open_brackets:
            return True

        # if self.token.string in ["class", "def"]:
        #     self.inside_class_or_def.append(self.token)
        #     self.class_or_def_indent = self.token.start_col
        #     return True

        # if self.inside_class_or_def:
        #     if self.token.start_col > self.class_or_def_indent:
        #         return True
        #     while self.inside_class_or_def:
        #         prev_class_or_def = self.inside_class_or_def.pop()
        #         self.class_or_def_indent = prev_class_or_def.start_col
        #         if self.token.start_col > self.class_or_def_indent:
        #             return True

        return False

    def init_export_statement(self):
        """Initialize relevant variables when a new potentially valid export
        statement is found.
        """
        self.reset_flags()
        self.begin_export = True
        self.current_row = self.token.start_row
        self.indentation = self.token.start_col
        self.export_stmt_info = {
            "indentation": self.indentation * " ",
            "row": self.current_row,
            "name": "",
            "export token": self.token,
        }

    def begin_new_statement(self):
        self.reset_flags()
        self.current_row = self.token.start_row
        if self.token == "export":
            self.begin_export = True

    def process_until_name_found(self):
        """Identify name to be exported"""
        if (
            self.token == "def" or self.token == "class"
        ) and self.prev_token == "export":
            self.export_class_or_def_name = True
            return

        if (
            self.prev_token == "def" or self.prev_token == "class"
        ) and self.token.is_identifier():
            self.export_stmt_info["name"] = self.token.string
            self.export_statements_info.append(self.export_stmt_info)
            self.reset_flags()
            return

        if (
            self.prev_token == "def" or self.prev_token == "class"
        ) and not self.token.is_identifier():
            self.reset_flags()
            return

        # Next, it's finding a variable name
        if (
            self.prev_token == "export"
            and self.token.is_identifier()
            and not self.export_variable
        ):
            self.export_variable = True
            if not self.export_stmt_info["name"]:
                # else, export is the (potential) identifier and we have "export export ..."
                self.export_stmt_info["name"] = str(self.token.string)
                # this token string needs to be converted as it will be altered later
            return

        if not self.export_variable:  # should not happen ... just to be safe ..
            self.reset_flags()

        if self.token == "=" and self.export_variable:
            self.export_statements_info.append(self.export_stmt_info)
            self.reset_flags()
        return

    def find_def_or_class_name(self):
        pass


def _display_location(info):
    """used for doing quick test at the terminal or debugging tests"""
    print(f"{len(info)=}")
    for entry in info:
        for item in entry:
            if item == "indentation":
                print(item, f"|{entry[item]}|")
            else:
                print(item, repr(entry[item]))
    print("-------------------")


def insert_all_info(new_tokens, current_info):

    new_all = """
{indent}__all__ = globals().setdefault("__all__", [])
{indent}__all__ = list(__all__)
{indent}__all__.append('{name}')
"""
    new_tokens.append(
        new_all.format(
            indent=current_info["indentation"],
            name=current_info["name"],
        )
    )
    return new_tokens


def transform_source(source, filename=None, callback_params=None, **kwargs):
    new_tokens = []

    if (
        filename != current_state.console_name
        and callback_params is not None
        and "public_dir" in callback_params
        and callback_params["public_dir"]
    ):
        intro = "__all__ = globals().setdefault('__all__', [])\n"
        intro += "__dir__ = lambda: __all__\n"
        source = intro + source

    info_locator = ExportInfo(source)
    info = info_locator.get_info()
    # _display_location(info)

    current_line = -1
    current_info = None
    prev_token = None
    changes_should_be_made = False

    if info:
        changes_should_be_made = True
        current_info = info.pop(0)  # important: need to pop from the beginning

    for token in token_utils.tokenize(source):
        if prev_token is None:
            new_tokens.append(token)
            prev_token = token
            continue

        if current_line != token.start_row:
            current_line = token.start_row

        if not current_info:  # we are done
            new_tokens.append(token)
            continue

        if current_info and prev_token.is_identical(current_info["export token"]):
            same_line_tokens = []
            while new_tokens:
                tok = new_tokens.pop()
                if tok.start_row == token.start_row:
                    if tok.is_identical(current_info["export token"]):
                        tok.string = token.string  # change export name
                    same_line_tokens.insert(0, tok)
                else:
                    new_tokens.append(tok)
                    break

            if filename != current_state.console_name:
                new_tokens = insert_all_info(new_tokens, current_info)
                new_tokens.extend(same_line_tokens)
            token.string = "      "  # length of export
            new_tokens.append(token)
            prev_token = token
            if info:
                current_info = info.pop(0)  # important: need to pop from the beginning
            else:
                current_info = None
            continue

        new_tokens.append(token)
        prev_token = token

    new_source = token_utils.untokenize(new_tokens)

    if changes_should_be_made:
        if new_source == source:
            print(
                "PROBLEM: changes to the source should have been made since 'info' is not empty!"
            )
    return new_source


def add_hook(public_dir=False, **_kwargs):
    from ideas import create_hook

    callback_params = {"public_dir": public_dir}

    return create_hook(
        transform_source=transform_source,
        callback_params=callback_params,
        name=__name__,
    )
