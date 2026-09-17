.. admonition:: Summary

   + We explain how to create a basic import hook.
   + We show how to do some simple source modification using ``token_utils``
   + We show how to use the ``-s`` or ``--show`` command line flag to get some
     debugging information.



Create your first import hook: the basics
=========================================

You've seen how to use |ideas| import hooks; now it is time to
create your first one.  Se use our ``"Hello world"`` example,
which uses ``function`` as equivalent to ``lambda``.


How to do this
---------------

Suppose you had access to the source of a program using
``function`` as a keyword instead of lambda.
Perhaps something like the following::

    # source of the program
    greet = function name: print(f"Hello {name}!")

So that you could write::

    >>> greet("World")
    Hello World!


Given access to that source, all you'd need to do is::

    modified_source = source.replace("function", "lambda")

and have Python execute ``modified_source`` instead of the original ``source``.


Here's how we can do it using |ideas|::

    from ideas import import_hook

    def some_arbitrary_name(source, **kwargs):
         return source.replace("function", "lambda")

    import_hook.create_hook(
        transform_source=some_arbitrary_name,
        name=__name__  # required
    )

That's it! Prior to having Python execute the source code,
ideas will take care of using the function ``some_arbitrary_name()``
to replace any occurrence of the name ``function`` by ``lambda``
so that the source code would contain only valid syntax.

While the code above would work, it is less than ideal as it would
replace the word ``function`` by ``lambda`` everywhere it occurs
in the source. Thus, given something like::

    """function.py

    This is a test demonstrating the use of our hook to replace
    function by lambda."""

    square = function x: x**2
    print(square(3))

If we attempted to do the following::

    >>> import function
    >>> help(function)

we would see this::

    lambda.py

    This is a test demonstrating the use of our hook to replace
    lambda by lambda.

This is far from ideal. There has to be a better way.

Actual code
------------

Here's the content of our real simplest example.

.. include:: ../../src/ideas/included/function_keyword.py
   :code: python

.. sidebar:: Tokens?

    Your Python code is a sequence of various operators
    (``+``, ``-``, ``:``, etc.), keywords, strings, etc.
    Each of these is an individual **token**.

``add_hook``
~~~~~~~~~~~~~

Rather than inserting our import hook immediately upon execution
of this module, we put the code to do so in the function
``add_hook``, and return the hook that was created.
This has at least four benefits:

    1. We can control when the hook is created.
    2. We can use the return value to change some of its parameters,
       for example to temporarily disable it, or to remove it 
       altogether. This can be particularly useful for testing.
    3. We can optionally add arguments to ``add_hook``; we will do so
       in more complex examples
    4. Perhaps the most import benefit is that, as we have seen before,
       we can invoke ideas from the command line with the
       ``-a`` or ``--add_hook`` flag,

.. code-block:: none

    ideas --add_hook function_keyword

which imports ``function_keyword`` and calls ``function_keyword.add_hook()``. 

Using ``token_utils``
~~~~~~~~~~~~~~~~~~~~~

To replace ``function`` by ``lambda`` only when it is meant to be
used as a keyword, we break up the code in a series of tokens
and only replace ``function`` by ``lambda`` when it occurs as
an individual token. Rather than using directly the tokenizer
from Python's standard library, we use our own version which has some useful
added features. For example, in almost all cases, the relevant
characteristic of a token is its string representation.
We can compare a token directly to a string like we did in the code above on line 16.

Note that, just like::

    def lambda():
        pass

would raise a ``SyntaxError``, the same would occur with::

    def function():
        pass

using our import hook.

Once we're done with replacing all ``function`` tokens by ``lambda``,
we convert the tokens back into a string by calling our
utility function ``untokenize`` on line 19.

Finally, **by convention**, we use the
same name, ``transform_source`` that is used as a keyword
argument for ``import_hook.create_hook``;
unlike ``add_hook``, using the specific name ``transform_source``
is not required by |ideas|.

Debugging help
~~~~~~~~~~~~~~

You can use the ``-s`` (or ``--show_changes``) flag to find out
what changes have been made by the source transformation to the original script;
a maximum of ten lines are shown.


.. code-block:: none

    > ideas -a function_keyword my_program -s -i

    #========== Original source from docs_examples/usage/my_program.py ====
    # flake8: noqa
    # my_program.py

    square = function x: x**2
    print(f"{square(4)} is the square of 4.")

    if __name__ == '__main__':
        print(f"And the square of 5 is {square(5)}")
    #=== End of Original source from docs_examples/usage/my_program.py ====


    #========== Transformed source ====
    # flake8: noqa
    # my_program.py

    square = lambda x: x**2
    print(f"{square(4)} is the square of 4.")

    if __name__ == '__main__':
        print(f"And the square of 5 is {square(5)}")
    #=== End of Transformed source ====

    16 is the square of 4.
    And the square of 5 is 25
    Ideas Console version 0.2.1. [Python version: 3.11.9]
    ideas>


For code entered at the console, only the changed source is shown.


.. code-block::

    ideas> cube = function x: x**3
    New: cube = lambda x: x**3

.. sidebar:: ``ideas_state``

    Because ``ideas_state`` often needs to be used to experiment
    with code in the console, it is available by default
    in the |ideas| console.

Inside the ideas console, you can turn on or off this feature
as follows::

    ideas> ideas_state.show_changes = False
    ideas> double = function x: 2*x
    ideas> ideas_state.show_changes = True
    ideas> triple = function x: 3*x
    New: triple = lambda x: 3*x
    ideas>


API for ``function_keyword``
----------------------------

.. automodule:: ideas.included.function_keyword
   :members:


Complete argument list for ``transform_source``
------------------------------------------------

In the above example, we had some unspecified keywords arguments
passed to ``transform_source``.

The last time this documentation was updated, the list of possible 
arguments could be found in the arguments of ``hook.transform_source``
below.

.. literalinclude:: ../../src/ideas/session.py
    :pyobject: State.source_transforms

``filename`` can sometimes be the name of the |ideas| console.

When using IPython or Jupyter, only the ``source`` is passed back to ``transform_source``.
