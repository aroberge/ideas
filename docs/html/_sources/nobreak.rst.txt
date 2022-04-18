.. admonition:: Summary

    Somewhat similar to the function keyword example except
    that we must keep track of the indentation level and
    replace our new keyword (``nobreak``) only if
    some conditions are met.


``nobreak`` as a keyword
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
to have ``nobreak`` as a keyword made the most sense.
It can be used instead of ``else`` in the above example::

    while condition:
        # some
        # code
        # here
    nobreak:
        # will be executed only if no
        # break statement occurred above


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

   *The optional else clause is executed if the control flow leaves the try suite,* **no exception was raised**, *and no* ``return``, ``continue``, *or* ``break`` *statement was executed.*

Since multiple causes can prevent the ``else`` clause from being executed,
it makes little sense in this case to use a different keyword such as
``nobreak``, that would point to a specific cause which would likely be wrong.

Useful function from ``token_utils``
-------------------------------------

The code for ``nobreak`` makes use of the ``get_first`` function from
``token_utils``. Here's some useful information about it.

.. code-block::

    >>> import token_utils
    >>> help(token_utils.get_first)
    Help on function get_first in module token_utils:

    get_first(tokens, exclude_comment=True)
        Given a list of tokens, find the first token which is not a space token
        (such as a ``NEWLINE``, ``INDENT``, ``DEDENT``, etc.) and,
        by default, also not a ``COMMMENT``.

        ``COMMMENT`` tokens can be included by setting ``exclude_comment`` to ``False``.

        Returns ``None`` if none is found.


API for ``nobreak``
----------------------------

.. automodule:: ideas.examples.nobreak
   :members:
