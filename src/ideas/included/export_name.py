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

from ideas import ideas_state
import token_utils as tu


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


def insert_all_info(export_info):

    new_all = """
{indent}__all__ = globals().setdefault("__all__", [])
{indent}__all__ = list(__all__)
{indent}__all__.append('{name}')
"""
    return new_all.format(
        indent=export_info["indentation"],
        name=export_info["name"],
    )


def transform_source(
    source, filename=None, callback_params=None, console_dict=None, **kwargs
):
    # Do we need pdir?
    if (
        filename != ideas_state.console_name
        and callback_params is not None
        and "public_dir" in callback_params
        and callback_params["public_dir"]
    ):
        intro = "__all__ = globals().setdefault('__all__', [])\n"
        intro += "__dir__ = lambda: __all__\n"
        source = intro + source

    new_lines = []
    stack = tu.IndentStack()

    for line in tu.get_logical_lines(source):
        first_token = line[0]
        if not first_token == "export":
            stack.update(line)
            new_lines.append(line)
            continue

        stack.update(line[1:])  # must not include "export"

        if stack.is_token_in_named_block(first_token, "class"):
            new_lines.append(line)
            continue
        elif stack.is_token_in_named_block(first_token, "def"):
            new_lines.append(line)
            continue

        second_token = line[1]
        if not second_token.is_in(["def", "class"]):
            if not second_token.is_identifier():
                new_lines.append(line)
                continue
            for token in line[2:]:
                if token == "=":
                    found_equal = True
                    break
            else:
                found_equal = False
            if not found_equal:
                new_lines.append(line)
                continue

        export_info = {"indentation": "", "name": ""}
        export_info["indentation"] = " " * line[0].indentation()
        line[0].string = line[1].string
        if line[1].is_in(["def", "class"]):
            export_info["name"] = line[2].string
        else:
            export_info["name"] = line[1].string
        line[1].string = ""

        new_lines.append([insert_all_info(export_info)])
        new_lines.append(line)

    return tu.stringify(new_lines)


def add_hook(public_dir=False, **_kwargs):
    from ideas import create_hook

    callback_params = {"public_dir": public_dir}

    return create_hook(
        transform_source=transform_source,
        callback_params=callback_params,
        name=__name__,
    )
