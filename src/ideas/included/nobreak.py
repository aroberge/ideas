"""
nobreak as a keyword
========================

Python's ``for`` and ``while`` loop include an ``else`` clause
whose meaning is not immediately obvious::

    while condition:
        # some
        # code
        # here
    else:
        # will be executed only if no
        # break statement occurred above

When I first understood this, I thought *wouldn't it be nice if, instead
of using* ``else:``, *one could write something like* ``if not break:`` which
uses only existing Python keywords.

For this example, I decided instead that a suggestion made by Raymond Hettinger
to have ``nobreak`` as a keyword made the most sense, even though I could just
as easily have used ``if no break`` instead.

So, with this import hook, ``nobreak`` can be used instead of ``else`` in the above example::

    while condition:
        # some
        # code
        # here
    nobreak:
        # will be executed only if no
        # break statement occurred above

This will be also the case for the optional ``else`` in a ``for`` loop.


``nobreak`` instead of ``else`` in ``if/else``
-------------------------------------------------------

The ``else`` keyword has a very different meaning when used as part
of an ``if`` statement.  In this situation, ``nobreak``, or its
translation in some other language would make no sense.

As a result, if one attempts to write the following::

    if condition:
        # some
        # code
        # here
    nobreak:
        # more code

``nobreak`` will **not** be replaced by ``else`` and
the code will raise a ``SyntaxError``.


What about try/except?
-----------------------

The ``else`` keyword can also be used in a ``try/except/else/finally`` block.
From `Python's documentation <https://docs.python.org/3/reference/compound_stmts.html#the-try-statement>`_:

   *The optional else clause is executed if the control flow leaves the try suite,*
   **no exception was raised**,
   *and no* ``return``, ``continue``, *or* ``break`` *statement was executed.*

Since multiple causes can prevent the ``else`` clause from being executed,
it makes little sense in this case to use a different keyword such as
``nobreak``, that would point to a specific cause which would likely be wrong.
"""

from ideas import create_hook
from token_utils import get_logical_lines, untokenize, IndentStack


def transform_source(source, **_kwargs):
    """``nobreak`` is replaced by ``else`` only if it is the first
    non-space token on a line and if its indentation matches
    that of a ``for`` or ``while`` block.
    """
    new_lines = []
    stack = IndentStack()
    stack.add_same_indent_keyword("nobreak")

    for line in get_logical_lines(source):
        top = stack.update(line)
        if top is None:
            new_lines.append(line)
            continue

        if line[0] == "nobreak" and top.is_in(["for", "while"]):
            line[0].string = "else"  # modify in place

        new_lines.append(line)

    return untokenize(new_lines)


def add_hook(**_kwargs):
    """Creates and automatically adds the import hook in sys.meta_path"""
    return create_hook(transform_source=transform_source, name=__name__)
