.. To avoid duplication, this is used both as a readme file for the
   function_simplest.py module and as contents of the documentation.

Create your own import hook
===========================

You've seen how to use ``ideas`` import hooks; now it is time to
create your first one.

.. admonition:: Description

    Suppose that you have no idea why ``lambda`` is used to define an anonymous
    function in Python and find it would be much more intuitive
    if you could use ``function`` as a keyword instead.
    So, you would like to create an import hook that would allow
    you to use ``function`` as a keyword in your own program and
    convert it to ``lambda`` before Python executes your code.


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


Here's how we can do it using ``ideas``::

    from ideas import import_hook

    def some_arbitrary_name(source, **kwargs):
         return source.replace("function", "lambda")

    import_hook.create_hook(transform_source=some_arbitrary_name)

That's it! Prior to having Python execute the source code, we made sure
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

.. literalinclude:: ../../ideas/examples/function_simplest.py
   :emphasize-lines: 7,12,16,19,21,22
   :linenos:

.. sidebar:: Tokens?

    Your Python code is a sequence of various operators
    (``+``, ``-``, ``:``, etc.), keywords, strings, etc.
    Each of these is an individual **token**.

Rather than inserting our import hook immediately upon execution
of this module, we put the code to do so in the function
``add_hook`` (line 19), and return the hook that was created (line 22).
This has at least three benefits:

    1. We can control when the hook is created.
    2. We can use the return value to remove the hook when it is no longer
       needed. This is useful for testing.
    3. We can add arguments to ``add_hook`` so as to modify what happens
       when our import hook is used. We will see some examples of
       this shortly.

To replace ``function`` by ``lambda`` only when it is meant to be
used as a keyword, we break up the code in a series of tokens
and only replace ``function`` by ``lambda`` when it occurs as
an individual token. Rather than using directly the tokenizer
from Python's standard library, we use our own version which has some useful
added features. For example, in almost all cases, the relevant
characteristic of a token is its string representation.
We can compare a token directly to a string like we did in the code above on line 12.

Note that, just like::

    def lambda():
        pass

would raise a ``SyntaxError``, the same would occur with::

    def function():
        pass

using our import hook.

Once we're done with replacing all ``function`` tokens by ``lambda``,
we convert the tokens back into a string by calling our
utility function ``untokenize`` on line 16.

Finally, to make our code easier to understand, on line 7 we use the
same name, ``transform_source`` that is used as a keyword
argument for ``import_hook.create_hook`` on line 21.
All of our examples follow this convention.
