"""

PEP 843
=======

PEP 843 suggests the addition of ``export`` as a soft keyword to be
used in expressions of the basic form::

    from x export y [as z]

with other slight variations described below. Assuming that
``__all__ = [...]`` is already defined, the statement

.. code-block::

    from x export y

would be equivalent to

.. code-block::

    from x import y
    __all__.append(y)

Implementation
--------------

We implement this as a source transformation. PEP 843 suggests that::

    from <module> import <name> as <alias>

should be equivalent to::

    from <module> import <name> as <alias>
    exported_names = globals().setdefault("__all__", [])
    if not isinstance(exported_names, list):
        exported_names = list(exported_names)
        __all__ = exported_names
    exported_names.append("<alias>")

We avoid introducing ``exported_names`` as an intermediary
variable by doing something like the following instead::

    from <module> import <name> as <alias>
    __all__ = globals().setdefault("__all__", [])
    __all__ = list(__all__)
    __all__.extend(["<alias>"])

PEP 843 also states that
"unlike ``import``, ``export`` is restricted to module level:
it’s a ``SyntaxError`` inside a ``def`` or ``class`` body."

As such, we do **not** transform ``from ... export ..`` if it occurs within
a class or function body.

Star version
-------------

For the star version::

    from module export *

we believe that something like the following should do what is expected::

    from [...]module import *
    __all__ = globals().setdefault("__all__", [])
    __all__ = list(__all__)
    from {relative} import {module}
    if hasattr({module}, "__all__"):
        __all__.extend(list({module}.__all__))
    else:
        for _ in dir({module}):
            if not _.startswith("_"):
                __all__.append(_)
        del _

lazy keyword
------------

While this transformation will insert "the right code" to replace::

    lazy from ... export ...

by::

    lazy from ... import ...
    # some additional code here

the additional code inserted in the case of an ``export *`` will result
in a non-lazy import. However, since this is just to provide a way to
test the syntax proposed in PEP 843, and not actually be used in production,
it should be no cause for concerns.

export as identifier
--------------------

``export`` can still be used as an identifier: it is only replaced by ``import``
on a top-level ``from ... export ...`` statement.

Example
-------

Suppose that we have the following file structure:

.. code-block:: none

    hub/
       __init__.py
       mod_a.py
       mod_b.py
       mod_c.py
       subhub/
           __init__.py
           mod_d.py

with the following file contents::

    # hub/__init__.py

    if True:
        from .mod_a export Widget, Gadget, export
    else:
        from .mod_a export NotWidget, NotGadget

    from .mod_b export *

    from .mod_c export (a,
        b,
    c
    )

    # mod_d defines __all__ as a tuple
    from .subhub.mod_d export *

.. code-block::

    # mod_a.py

    class Widget:
        pass

    class Gadget:
        pass

    class NotWidget:
        pass

    class NotGadget:
        pass

    export = "safe name"

.. code-block::

    # mod_b.py

    def cool():
        pass

    def _cool():
        pass

    def hot():
        pass

    def _hot():
        pass

.. code-block::

    # mod_c.py

    a = b = c = d = e = 1

.. code-block::

    # mod_d.py

    spam = "spam"
    ham = "ham"
    not_spam = "not_spam"
    not_ham = "not_ham"

    # Note the use of a tuple instead of a list.
    __all__ = ("spam", "ham")

Here is what an interactive session with the Ideas console
looks like:

.. code-block:: none

    (venv-ideas3.11) C:\\Users\\Andre\\github\\ideas
    > python -i -m ideas -a pep_843
    Ideas Console version 0.2.0. [Python version: 3.11.9]
    ideas> from hub import *
    ideas> dir()
    ['Gadget', 'Widget', '__builtins__', 'a', 'b', 'c', 'cool', 'current_state', 'export', 'ham', 'hot', 'spam']
    ideas> export
    'safe name'
    ideas>

And here's a similar experiment done within the normal Python repl:

.. code-block:: none

    > py
    Python 3.11.9 ...
    >>> from ideas.examples.pep_843 import add_hook
    >>> hook = add_hook()
    >>> from hub import *
    >>> dir()
    ['Gadget', 'Widget', '__annotations__', '__builtins__', '__doc__', '__loader__', '__name__', '__package__', '__spec__', 'a', 'add_hook', 'b', 'c', 'cool', 'export', 'ham', 'hook', 'hot', 'spam']
    >>> export
    'safe name'
    >>>

.. warning::

    Do not use continuation characters. The current transformation might not handle
    them correctly.

"""

import sys
from ideas.utils import get_significant_tokens
import token_utils

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
        self.from_statements_info = []
        self.from_stmt_info = {}
        self.indentation = 0
        self.current_row = -1
        self.begin_from = False
        self.inside_class_or_def = []
        self.open_brackets = []  # Any ([{ open but not closed
        self.class_or_def_indent = -1
        self.prev_token = None
        self.open_parens = []  # inside from ... import (...)

    def get_info(self):
        for self.token in get_significant_tokens(self.source):

            if not self.begin_from:
                if self.skip_over_irrelevant_token():
                    self.prev_token = self.token
                    continue

            if self.token == "from":
                self.init_from_statement()
                self.prev_token = self.token
                continue

            if self.token.start_row > self.current_row and not self.open_parens:
                self.begin_new_statement()
                self.prev_token = self.token
                continue

            if not self.begin_from:
                self.prev_token = self.token
                continue

            if not self.export_found:
                self.process_until_export_statement()
                self.prev_token = self.token
                continue

            self.process_end_of_from_statement()
            self.prev_token = self.token

        # if from statement was last statement of source, we need to add it.
        if self.from_stmt_info:
            self.from_statements_info.append(self.from_stmt_info)
        return self.from_statements_info

    def skip_over_irrelevant_token(self):
        if self.token.string in "([{":
            self.open_brackets.append(self.token.string)
            return True
        elif self.token.string in ")]}":
            self.open_brackets.pop()
            return True
        elif self.open_brackets:
            return True

        if self.token.string in ["class", "def"]:
            self.inside_class_or_def.append(self.token)
            self.class_or_def_indent = self.token.start_col
            return True

        if self.inside_class_or_def:
            if self.token.start_col > self.class_or_def_indent:
                return True
            while self.inside_class_or_def:
                prev_class_or_def = self.inside_class_or_def.pop()
                self.class_or_def_indent = prev_class_or_def.start_col
                if self.token.start_col > self.class_or_def_indent:
                    return True

        return False

    def init_from_statement(self):
        """Initialize relevant variables when a new from statement is found."""
        if self.begin_from:
            if self.from_stmt_info:
                self.from_statements_info.append(self.from_stmt_info)
        self.begin_from = True
        self.current_row = self.token.start_row
        self.indentation = self.token.start_col
        if self.prev_token == "lazy":
            self.indentation = self.prev_token.start_col
        self.from_stmt_info = {
            "indentation": self.indentation * " ",
            "row": self.current_row,
            "next row": self.current_row + 1,
            "public names": [],
            "module name": "",
            "export token": None,
        }
        self.export_found = False

    def begin_new_statement(self):
        if self.begin_from:
            self.from_statements_info.append(self.from_stmt_info)
            self.from_stmt_info = {}
        self.current_row = self.token.start_row

    def process_until_export_statement(self):
        """Identify module name and if export/import is used"""
        if self.token == "import":  # drop everything for this line
            self.begin_from = False
            self.from_stmt_info = {}
            return

        elif self.token == "export":
            self.export_found = True
            self.from_stmt_info["export token"] = self.token
            return

        self.from_stmt_info["module name"] += self.token.string
        return

    def process_end_of_from_statement(self):
        """Identify public names after export keyword"""
        self.current_row = self.token.start_row
        if self.token.is_identifier():
            if self.prev_token == "as":
                self.from_stmt_info["public names"].pop()
            self.from_stmt_info["public names"].append(self.token.string)
        elif self.token == "(":
            self.open_parens.append(self.token)
        elif self.token == ")":
            self.open_parens.pop()
            if not self.open_parens:  # this should be the case
                self.from_stmt_info["next row"] = self.current_row + 1
        elif self.token == "*":
            self.from_stmt_info["public names"] = "*"


def _display_location(info):
    """used for doing quick test at the terminal or debugging tests"""

    for entry in info:
        for item in entry:
            if item == "indentation":
                print(item, f"|{entry[item]}|")
            elif item == "export token":
                print(item, repr(entry[item]))
            else:
                print(item, entry[item])
        print()


def insert_all_info(new_tokens, current_info):

    new_all = """
{indent}__all__ = globals().setdefault("__all__", [])
{indent}__all__ = list(__all__)
{indent}__all__.extend({names})
"""

    new_all_star = """
{indent}__all__ = globals().setdefault("__all__", [])
{indent}__all__ = list(__all__)
{indent}from {relative} import {module}
{indent}if hasattr({module}, "__all__"):
{indent}    __all__.extend(list({module}.__all__))
{indent}else:
{indent}    for _ in dir({module}):
{indent}        if not _.startswith("_"):
{indent}            __all__.append(_)
{indent}    del _
"""

    if current_info["public names"] == "*":
        module = current_info["module name"]
        nb_dots = module.count(".")
        if nb_dots < 2:
            relative = "."
            module = module.split(".")[-1]
        else:
            split = module.split(".")
            module = split[-1]
            relative = ".".join(split[:-1])

        new_tokens.append(
            new_all_star.format(
                indent=current_info["indentation"],
                module=module,
                relative=relative,
            )
        )
    else:
        new_tokens.append(
            new_all.format(
                indent=current_info["indentation"],
                names=current_info["public names"],
            )
        )

    return new_tokens


def transform_source(source, **kwargs):
    new_tokens = []

    info_locator = ExportInfo(source)
    info = info_locator.get_info()
    # _display_location(info)

    current_info = None

    if info:
        current_info = info.pop(0)

    for token in token_utils.tokenize(source):
        if current_info is None or current_info["row"] > token.start_row:
            new_tokens.append(token)
            continue

        if token.is_identical(current_info["export token"]):
            token.string = "import"
            new_tokens.append(token)
            continue

        if token.start_row == current_info["next row"]:
            if new_tokens[-1] == "\n":
                new_tokens.pop()
            new_tokens = insert_all_info(new_tokens, current_info)
            if info:
                current_info = info.pop(0)
            else:
                current_info = None
        new_tokens.append(token)

    if current_info is not None:
        new_tokens = insert_all_info(new_tokens, current_info)
    new_source = token_utils.untokenize(new_tokens)

    if "pytest" in sys.modules:
        if source != new_source:
            print("\n====== Original source for pep_843 ============")
            print(source)
            print("-----------------")
            print("\n====== New source ============")
            print(new_source)
            print("-----------------")
        else:
            print("No change in source")
    return new_source


def add_hook(**_kwargs):
    from ideas import create_hook

    return create_hook(transform_source=transform_source, name=__name__)
