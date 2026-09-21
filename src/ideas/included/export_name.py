"""
This import hook was **inspired** by
`PEP 842 (withdrawn) <https://peps.python.org/pep-0842/>`_
which suggested the addition of ``export`` as a soft keyword
to be used in the following three cases::

    export name ... = ...
    export def function_name(): ...
    export class ClassName(): ...


.. sidebar:: Competing PEP

   We note that `PEP 844 <https://peps.python.org/pep-0844/>`_
   propose the inclusion of functions defined in the
   ``at_public`` project as Python builtins with a
   similar goal, i.e. automatically updating ``__all__``
   while enabling people reading the source code to
   easily identify which names are meant to be public.

Note that PEP 842 suggests a lot more than what we wrote above:

+ It suggest the creation of an ``__export__`` list.
+ It suggest that using ``export`` other than in top-level statement
  should result in an ``ExportError``.
+ It suggests the creation of a modified ``__dir__``.
+ etc.

We will first start with an example that implements only the
three cases we mentioned. Consider the following file:

.. code-block::

    # export_name_1.py

    from math import pi

    export PI = pi

    export public = "public variable"

    export def useful_fn():
        print("This is a very useful function")

    def private():
        print("I want to be able to change my name.")

    secret = "Ideas's code is a mess."

Let's use our import hook to import this function using a
standard Python interpreter.

.. code-block::

    > py
    Python 3.11.9 ...
    >>> from ideas.included.export_name import add_hook
    >>> hook = add_hook()
    >>> import export_name_1
    >>> dir(export_name_1)
    ['PI', '__all__', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'pi', 'private', 'public', 'secret', 'useful_fn']

Looking closely at the output, we can see that ``private``, ``pi``, and ``secret``
which were not meant to be exposed are still visible and are available.

.. code-block::

    >>> export_name_1.secret
    "Ideas's code is a mess."

And, ``__all__`` only shows the names we want, so we could quickly determine
if it is safe to use a star-import.

    >>> export_name_1.__all__
    ['PI', 'public', 'useful_fn']

A restricted ``dir``
--------------------

As we can see from the example above, when simply using ``dir``, which is what a Python
programmer normally does to see the avaiable names, it might be difficult to identify
which names are "public". Presumably for this reason, PEP 842 suggests that using ``export``
in a module should also result in creating a ``__dir__`` function within this module so that
Python's ``dir`` function can be restricted to only show the desired names.

We have implemented a version of this idea, available as an option, demonstrated
below.

.. code-block::

    > py
    Python 3.11.9 ...
    >>> from ideas.included.export_name import add_hook
    >>> hook = add_hook(public_dir=True)  # optional argument
    >>> import export_name_1
    >>> dir(export_name_1)
    ['PI', 'public', 'useful_fn']

This is indeed the desired result.
We can nonetheless still see all the available names that ``dir`` would have shown us before
using ``vars``.

.. code-block::

    >>> list(vars(export_name_1))
    ['__name__', '__doc__', '__package__', '__loader__', '__spec__', '__file__', '__cached__', '__builtins__', '__all__', '__dir__', 'pi', 'PI', 'public', 'useful_fn', 'private', 'secret']

Instead of creating a ``__dir__`` function within the module, we prefer to use a simple function
that we have written, which extracts the content of ``__all__`` if it exists, otherwise it
gives us what ``dir`` would give us normally, but not always in the same order.

.. code-block::

    > py
    Python 3.11.9 ...
    >>> from ideas.included.export_name import pdir
    >>> pdir()
    ['__name__', '__doc__', '__package__', '__loader__', '__spec__', '__annotations__', '__builtins__', 'pdir']
    >>> pdir().sort() == dir().sort()
    True
    >>> from ideas.included.export_name import add_hook
    >>> hook = add_hook()
    >>> import export_name_1
    >>> dir(export_name_1)
    ['PI', '__all__', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'pi', 'private', 'public', 'secret', 'useful_fn']

    >>> pdir(export_name_1)
    ['PI', 'public', 'useful_fn']

As we can see, with a simple utility function, like ``pdir``, we do not use to create a special
``__dir__`` within a module.


Implementation
---------------

Let's explore how this is implemented, like we did in the
:doc:`from ... export (PEP 843) <./from_export>` import hook.

.. code-block::

    > py
    Python 3.11.9 (tags/v3.11.9:de54cf5, Apr  2 2024, 10:12:12) [MSC v.1938 64 bit (AMD64)] on win32
    Type "help", "copyright", "credits" or "license" for more information.
    >>> from ideas import transform
    >>> from ideas.included.export_name import add_hook
    >>> hook = add_hook()
    >>> transform("export def test(): ...")

    __all__ = globals().setdefault("__all__", [])
    __all__ = list(__all__)
    __all__.append('test')
    def        test(): ...

We would have a similar result with ``class`` instead of ``def``.
The situation is slightly different for variables.
First, a proper declaration.

.. code-block::

    >>> transform("export name = ...")

    __all__ = globals().setdefault("__all__", [])
    __all__ = list(__all__)
    __all__.append('name')
    name        = ...

However, if not assignment is done using an ``=`` sign,
no transformation takes place.


    >>> transform("export name ...")
    export name ...

The same occurs if an ``export`` keyword is not used at the top level.

.. code-block::

    >>> transform("export name ...")
    export name ...
    >>> source = '''
    ... def test():
    ...     export name = 'Bob'
    ... '''
    >>> transform(source)

    def test():
        export name = 'Bob'

This would clearly cause a syntax error if it were to be executed.

Finally, let us give a single additional example with the ``public_dir``
option. However, we can't simply use the ``transform`` function as
it only takes a source as an argument and we need to tell
our import hook other arguments to take into account.
However, we can import a file, defined as follows:

.. code-block::

    # flake8: noqa
    # export_name_2.py
    export name = 'Bob'

We'll use the |ideas| command line so as to reduce the amount
of typing required.

.. code-block::

    > ideas -a export_name -s export_name_2 --callback_params public_dir=True

    #========== Original source from docs_examples/export_name/export_name_2.py ====
    # flake8: noqa
    # export_name_2.py
    export name = 'Bob'
    #=== End of Original source from docs_examples/export_name/export_name_2.py ====


    #========== Transformed source ====
    __all__ = globals().setdefault('__all__', [])
    __dir__ = lambda: __all__
    # flake8: noqa
    # export_name_2.py

    __all__ = globals().setdefault("__all__", [])
    __all__ = list(__all__)
    __all__.append('name')
    name        = 'Bob'
    #=== End of Transformed source ====

As we can see, at the top of the transformed source, a new ``__dir__`` function
has been introduced.

"""

from ideas.utils import get_significant_tokens
import token_utils
from ideas import ideas_state


def pdir(obj=None):
    """Returns the contents of ``__all__`` if available,
    if not returns what ``dir`` would."""
    import inspect

    if obj is not None:
        if hasattr(obj, "__all__"):
            return obj.__all__
        return dir(obj)

    caller_frame = inspect.currentframe().f_back
    caller_locals = caller_frame.f_locals if caller_frame else {}
    if obj is None:
        if "__all__" in caller_locals:
            return caller_locals["__all__"]
        else:
            return list(caller_locals)  # only the keys


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
        self.inside_class_or_def = False
        self.open_brackets = []  # Any ([{ open but not closed
        self.class_or_def_indent = 0
        self.prev_token = None
        self.reset_flags()
        self.first_row_token = None

    def reset_flags(self):
        self.begin_export = False
        self.export_class_or_def_name = False
        self.export_variable = False
        self.export_stmt_info = {}

    def get_info(self):
        for self.token in get_significant_tokens(self.source):
            if self.prev_token and self.token.start_row != self.prev_token.start_row:
                self.first_row_token = self.token

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

        if not self.inside_class_or_def:
            return False

        if self.token.start_col > self.class_or_def_indent:
            return True

        if self.token.string in ["class", "def"]:
            self.class_or_def_indent = self.token.start_col
            return True
        elif not (
            self.first_row_token.is_keyword() or self.first_row_token.is_identifier()
        ):
            return True
        else:
            self.inside_class_or_def = False
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
        elif self.token.string in ["class", "def"]:
            self.class_or_def_indent = self.token.start_col
            self.inside_class_or_def = True

    def process_until_name_found(self):
        """Identify name to be exported"""
        if (
            self.token == "def" or self.token == "class"
        ) and self.prev_token == "export":
            self.export_class_or_def_name = True
            if not self.inside_class_or_def:
                self.inside_class_or_def = True
                # the indentation was determined by "export"
                self.class_or_def_indent = self.prev_token.start_col
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


def transform_source(
    source, filename=None, callback_params=None, console_dict=None, **kwargs
):
    new_tokens = []

    if (
        filename != ideas_state.console_name
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

            if filename != ideas_state.console_name:
                new_tokens = insert_all_info(new_tokens, current_info)
            elif console_dict is not None:
                if "__all__" not in console_dict:
                    console_dict["__all__"] = [current_info["name"]]
                else:
                    console_dict["__all__"].append[current_info["name"]]
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
