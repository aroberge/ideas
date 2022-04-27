"""

.. admonition:: Summary

   This example illustrates how one can change the indentation
   of an entire block of code, eliminate lines, and change the
   content much more drastically than what the previous
   examples have done.

   The idea behind this example is to help reduce the amount of typing
   required and increases readability when assigning attributes in a
   class's ``__init__()`` method.

Auto self
==========

Python is known for its concise and readable syntax. One exception
about the concisiveness is the boiler plate code that has to be
written when defining one's own class, especially if it has
many attributes, like::

    self.this_variable = this_variable
    self.that_variable = that_variable
    self.this_other_variable = this_other_variable
    self.foo = foo
    self.bar = bar

    self.baz = [] if baz is None else baz
    self.spam = bread + ham


This leads people to ask on various forums, such as
`this question on StackOverflow <https://stackoverflow.com/questions/3652851/what-is-the-best-way-to-do-automatic-attribute-assignment-in-python-and-is-it-a>`_,
how to do automatic assignment of attributes.  The answers most often given
are:

  - Don't do it; learn to live with the explicit ``self``.
  - Use a decorator, with various examples provided.


As programmers create more classes, they find the need to add their own
dunder methods, such as ``__eq__(self, other)``, ``__repr__(self)``, etc.
Eventually, they might get annoyed enough at having to re-create these methods
too often, with the occasional typo causing bugs that they jump with
joy when discovering `attrs: Classes Without Boilerplate <https://www.attrs.org/en/stable/>`_.

Starting with Python 3.7, the standard library includes
`dataclasses <https://docs.python.org/3/library/dataclasses.html>`_ which shares some
similarity with ``attrs``. However, it does require to use type hints which,
in my opinion, reduces readability; note that many programmers find that
type hints increase readability.

As a concrete example of using traditional Python notation and
dataclasses, let's consider the code given in
`PEP 557  <https://www.python.org/dev/peps/pep-0557/>`_ but reformatted with Black::

    class Application:
        def __init__(
            self,
            name,
            requirements,
            constraints=None,
            path="",
            executable_links=None,
            executables_dir=(),
        ):
            self.name = name
            self.requirements = requirements
            self.constraints = {} if constraints is None else constraints
            self.path = path
            self.executable_links = [] if executable_links is None else executable_links
            self.executables_dir = executables_dir
            self.additional_items = []

From the same PEP document, this is the proposed code
which gives the same initialization, but using the ``@dataclass``
decorator::

    from dataclasses import dataclass

    @dataclass
    class Application:
        name: str
        requirements: List[Requirement]
        constraints: Dict[str, str] = field(default_factory=dict)
        path: str = ''
        executable_links: List[str] = field(default_factory=list)
        executable_dir: Tuple[str] = ()
        additional_items: List[str] = field(init=False, default_factory=list)


This code does more than simply initializing the variables, but I
do not find it particularly readable.

So, I was wondering if it might be possible to imagine a simpler syntax.
``auto_self`` is what I came up with.

.. admonition:: That ship has sailed ...

    I realize that there is zero chance that the following syntax would
    be adopted, especially now that the ``dataclasses`` module has been added to
    the Python standard library. Still, you can try it out using
    ``auto_self`` hook.

.. code-block:: python

    class Application:
        def __init__(
            self,
            name,
            requirements,
            constraints=None,
            path="",
            executable_links=None,
            executables_dir=(),
        ):
            self .= :
                name
                requirements
                constraints = {} if __ is None else __
                path
                executable_links = [] if __ is None else __
                executables_dir
                additional_items = []

Here, I am using a new operator, ``.=``, which is meant to represent
the automatic assignment of a variable to the name that precedes
it (``self`` in this example).  I have seen this idea for such an operator before on
**python-ideas** but never for introducing a code block as I do here.

By design, any *dunder* (double underscore), ``__``, is taken to be equivalent to the variable
being initialized.  I chose a dunder instead of a single underscore ``_``
so that it could be used in a REPL without creating conflicts with the
existing use of a single underscore in Python's REPL.  I also find that it
makes it more readable.

Of course, one is not restricted to using ``self``, or having to use ``__``
everywhere. The following is completely equivalent - although I now
find it less readable, having been used to seeing ``__`` as easy to scan
placeholder::


    class Application:
        def __init__(
            cls,
            name,
            requirements,
            constraints=None,
            path="",
            executable_links=None,
            executables_dir=(),
        ):
            cls .= :
                name
                requirements
                constraints = {} if constraints is None else constraints
                path
                executable_links = [] if __ is None else executable_links
                executables_dir

            cls.additional_items = []

.. warning::

    Unlike ``@dataclass`` or ``attrs``, no additional method is
    created by ``auto_self``.

"""
from ideas import import_hook
import token_utils


def transform_source(source, **_kwargs):
    """Replaces code like::

        self .= :
            a
            b
            c = this if __ == that else ___

    by::

        self.a = a
        self.b = b
        self.c = this if c == that else c
    """
    new_tokens = []
    auto_self_block = False
    self_name = ""
    indentation = 0

    get_nb = token_utils.get_number
    get_first = token_utils.get_first
    get_first_index = token_utils.get_first_index

    for tokens in token_utils.get_lines(source):
        if auto_self_block:
            variable = get_first(tokens)
            if variable is not None:  # None would mean an empty line
                var_name = variable.string
                block_indent = variable.start_col
                if block_indent > indentation:
                    dedent = block_indent - indentation
                    if get_nb(tokens) == 1:
                        variable.string = f"{self_name}.{var_name} = {var_name}"
                        tokens = token_utils.dedent(tokens, dedent)
                    else:
                        variable.string = f"{self_name}.{var_name}"
                        for token in tokens:
                            if token.string == "__":
                                token.string = var_name
                        tokens = token_utils.dedent(tokens, dedent)
                else:
                    auto_self_block = False
        elif get_nb(tokens) == 4:
            index = get_first_index(tokens)
            if (
                tokens[index].is_identifier()
                and tokens[index + 1] == "."
                and tokens[index + 2] == "="
                and tokens[index + 1].end_col == tokens[index + 2].start_col
                and tokens[index + 3] == ":"
            ):
                self_name = tokens[index].string
                indentation = tokens[index].start_col
                auto_self_block = True
                continue
        new_tokens.extend(tokens)
    return token_utils.untokenize(new_tokens)


def add_hook(**_kwargs):
    """Creates and adds the import hook in sys.meta_path"""
    hook = import_hook.create_hook(
        transform_source=transform_source,
        hook_name=__name__,
    )
    return hook
