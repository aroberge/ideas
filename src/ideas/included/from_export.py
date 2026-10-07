"""
`PEP 843 <https://peps.python.org/pep-0843/>`_
suggests the addition of ``export`` as a soft keyword to be
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

The main motivation of this PEP appears to be facilitating the
maintenance of "large projects" which define their public interface
within an ``__init__.py`` file, by importing various objects
from the "private" subdirectories and exposing them to the public.
This requires updating ``__all__`` each time a new variable is
to be made public.

This import hook implements a source transformation that aims
to mimic the proposed changes described in PEP 843.


Example
-------

The code in this section is from an example that we currently
did with this import hook.

Suppose that we have the following file structure:

.. code-block:: none

    hub/
       __init__.py
       mod_a.py
       mod_b.py
       _internal/
           __init__.py
           mod_c.py

with the following file contents::

    # hub/__init__.py

    from hub.mod_a export Widget, Gadget as NewGadget, export

    from hub.mod_b export (a,
        b,
        c,
    )

    # mod_c defines __all__ as a tuple
    from hub._internal.mod_c export *


.. code-block::

    # hub/mod_a.py

    class Widget: pass

    class Gadget: pass

    class NotWidget: pass

    class NotGadget: pass

    export = "A safe name"

.. code-block::

    # hub/mod_b.py

    a = b = c = d = e = f = g = 1

.. code-block::

    # hub/_internal/mod_c.py

    spam = "spam"
    ham = "ham"
    not_spam = "not_spam"
    not_ham = "not_ham"

    # Note the use of a tuple instead of a list.
    __all__ = ("spam", "ham")

Here is what an interactive session with the Ideas console
looks like:

.. code-block:: none

    > ideas -a from_export
    Ideas Console version 0.3.4. [Python version: 3.11.9]
    ideas> dir()
    ['__builtins__', 'ideas_state']
    ideas> from hub import *
    ideas> dir()
    ['NewGadget', 'Widget', '__builtins__', 'a', 'b', 'c', 'export', 'ham', 'ideas_state', 'spam']
    ideas> export  # variable name unaffected
    'A safe name'

As we can verify, only the names that were meant to be "exported" have been imported.

And here's a similar experiment done using the normal Python repl:

.. code-block:: none

    >>> from ideas.included.from_export import add_hook
    >>> hook = add_hook()
    >>> import hub
    >>> hub.__all__
    ['Widget', 'NewGadget', 'export', 'a', 'b', 'c', 'spam', 'ham']

Proposed implementation
-----------------------

PEP 843 suggests that::

    from <module> export <name> as <alias>

should be equivalent to::

    from <module> import <name> as <alias>
    exported_names = globals().setdefault("__all__", [])
    if not isinstance(exported_names, list):
        exported_names = list(exported_names)
        __all__ = exported_names
    exported_names.append("<alias>")

We implement something similar as a source transformation.
However, we avoid introducing ``exported_names`` as an intermediary.

PEP 843 also states that
"unlike ``import``, ``export`` is restricted to module level:
it’s a ``SyntaxError`` inside a ``def`` or ``class`` body."

As such, we do **not** transform ``from ... export ..`` if it occurs within
a class or function body. Such code **will** result in a ``SyntaxError``.

Actual implementation of this import hook
------------------------------------------

To see the actual implementation, we can use the recently
added command line option ``--t`` of the |ideas| entry point
to quickly see the result.

First, we consider an "export" statement with names fully specified,
and arbitrarily indented to illustrate that the indentation
is preserved.

.. code-block::

    > ideas -a from_export -t "       from a.b export A, B as C"
        from a.b import A, B as C
        __all__ = globals().setdefault("__all__", [])
        __all__ = list(__all__)
        __all__.extend(['A', 'C'])

Next, we look at the star version:

.. code-block::

    > ideas -a from_export -t "from module export *"
    from module import *
    __all__ = globals().setdefault("__all__", [])
    __all__ = list(__all__)
    from . import module
    if hasattr(module, "__all__"):
        __all__.extend(list(module.__all__))
    else:
        for _ in dir(module):
            if not _.startswith("_"):
                __all__.append(_)
        del _

Looking ahead we can also support the ``lazy`` keyword.

.. code-block::

    > ideas -a from_export -t "lazy from math export pi"
    lazy from math import pi
    __all__ = globals().setdefault("__all__", [])
    __all__ = list(__all__)
    __all__.extend(['pi'])


export as an identifier
------------------------

As we have seen in the example above ``export`` can still be used as an identifier:
it is only replaced by ``import``
**on a top-level** ``from ... export ...`` statement.
Using such a statement anywhere else will result in a ``SyntaxError`` when
the code is executed by Python.
In the following example, we demonstrate this.
Since we need to use a multiline example with indentation, we cannot
do it with the ``-t`` option on the command line.

.. code-block:: none

    ideas> from ideas import transform
    ideas> with open("from_export_1.py", "r") as f:
    ...     source = f.read()
    ...
    ideas> print(source)
    # from_export_1.py

    def test():
        from math export pi

    ideas> transform(source)
    # from_export_1.py

    def test():
        from math export pi


We can see that no source transformation took place.
Now, let's try to import this file:

.. code-block:: none

    ideas> import from_export_1
    File "C:\\Users\\Andre\\github\\ideas\\docs_examples\\included\\from_export\\from_export_1.py", line 4
        from math export pi
                  ^^^^^^
    SyntaxError: invalid syntax
"""

from ideas import ideas_state
import token_utils as tu


def insert_all_info(new_tokens, export_info):

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

    if export_info["public names"] == ["*"]:
        module = export_info["module name"]
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
                indent=export_info["indentation"],
                module=module,
                relative=relative,
            )
        )
    else:
        new_tokens.append(
            new_all.format(
                indent=export_info["indentation"],
                names=export_info["public names"],
            )
        )

    return new_tokens


def transform_source(source, filename=None, **_kwargs):
    new_lines = []
    stack = tu.IndentStack()

    for line in tu.get_logical_lines(source):
        stack.update(line)
        first_token = line[0]
        # Lines that are NOT of the form "from ... export"
        # or which are inside a class or def block
        # are left unchanged
        if first_token != "from" and not (first_token == "lazy" and line[1] == "from"):
            new_lines.append(line)
            continue
        elif stack.is_token_in_named_block(first_token, "class"):
            new_lines.append(line)
            continue
        elif stack.is_token_in_named_block(first_token, "def"):
            new_lines.append(line)
            continue

        found_export = False
        for token in line:
            if token == "import":
                break
            elif token == "export":
                found_export = True
                break
        if not found_export:
            new_lines.append(line)
            continue

        # Focus on line from ... export
        found_export = False
        found_from = False
        export_info = {"indentation": "", "public names": [], "module name": ""}
        for tok1, tok2, tok3 in tu.sliding_window(line, 3):

            if not found_from and (tok1 == "from" or tok1 == "lazy"):
                export_info["indentation"] = " " * tok1.indentation()
                found_from = True
                continue

            if tok1 == "export":
                tok1.string = "import"
                if tok3 != "as" and tok2.is_identifier() or tok2 == "*":  # could be (
                    export_info["public names"].append(tok2.string)
                found_export = True
                continue

            if not found_export:
                export_info["module name"] += tok1.string
                continue

            if tok1.is_in([",", "("]) and tok2.is_identifier() and tok3 != "as":
                export_info["public names"].append(tok2.string)
            elif tok2 == "as":
                export_info["public names"].append(tok3.string)

        # To have a more predictable output, we remove a new line
        line[-1].string = ""
        new_lines.append(line)
        new_line = insert_all_info([], export_info=export_info)

        # can't process multiple lines in the console
        if filename != ideas_state.console_name:
            new_lines.append(new_line)
        else:
            print(tu.stringify(new_line))
    return tu.stringify(new_lines)


def add_hook(**_kwargs):
    from ideas import create_hook

    return create_hook(transform_source=transform_source, name=__name__)
