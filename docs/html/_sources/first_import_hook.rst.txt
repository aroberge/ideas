.. admonition:: Summary

   + We explain how to create a basic import hook.
   + We show how to do some simple source modification using ``token_utils``.
   + We show how to use the ``-s`` or ``--show_changes`` command line flag to get some
     debugging information.



Create your first import hook: the basics
=========================================

You've seen how to use |ideas| import hooks; now it is time to
create your first one.  We will use our ``"Hello world"`` example,
which uses ``function`` as equivalent to ``lambda``.


How use do this
---------------

Suppose you had access to the source of a program using
``function`` as a keyword instead of lambda.
Perhaps something like the following:

.. include:: ../../docs_examples/first_import_hook/greet_script.py
   :code: python

So that you could write::

    >>> import greet_script
    Hello World!


If you had access to that source, all you would need to do is::

    modified_source = source.replace("function", "lambda")

and have Python execute ``modified_source`` instead of the original ``source``.

Here's how we can do it using |ideas|:

.. include:: ../../docs_examples/first_import_hook/simple_replacement.py
   :code: python

That's it! Let's try it out.

.. code-block::

    >>> import greet_script  # of course, this won't work
    Traceback (most recent call last):
    File "<stdin>", line 1, in <module>
    File "C:\Users\Andre\github\ideas\docs_examples\first_import_hook\greet_script.py", line 6
        greet = function name: print(f"Hello {name}!")
                        ^^^^
    SyntaxError: invalid syntax
    >>> import simple_replacement  # sets up the import hook
    >>> import greet_script
    Hello World!


It works! ... almost ... Let's find out more::

    >>> help(greet_script)
    Help on module greet_script:

    NAME
        greet_script - greet_script.py

    DESCRIPTION
        This is a test demonstrating the use of our hook to replace
        lambda by lambda.

    FUNCTIONS
        greet lambda name

    FILE
        c:\\users\\andre\\github\\ideas\\docs_examples\\first_import_hook\\greet_script.py

Something is not ideal with the DESCRIPTION: it says that it replaces
``lambda`` by ``lambda``, which is not very helpful.
Still, as a first step, it shows how easy it is to write an
import hook that modifies the source code using |ideas|.
Instead of importing everything within a standard Python
interpreter, let's execute the code using |ideas| on the command line.

.. code-block:: none

    > ideas -a simple_replacement greet_script
    Module <module 'simple_replacement' from 'C:\\Users\\Andre\\github\\ideas\\docs_examples\\first_import_hook\\simple_replacement.py'> does not contain a function named add_hook
    Hello World!

Something is not quite right: using the ``-a`` flag told |ideas| to import
the module (which it did), then find the ``add_hook`` function and execute it.
However, our example did not have such a function defined, as it directly
created an import hook which was then used to replace ``function`` by
``lambda`` when the file ``greet_script.py`` was executed.
So, in spite of the error message from |ideas|,
everything worked the way we wanted when it came to replace ``function`` by ``lambda``.

Actual code
------------

Here's the content of the similar import hook included in
|ideas| when you install it on your computer.

.. include:: ../../src/ideas/included/function_keyword.py
   :code: python

``add_hook``
~~~~~~~~~~~~~

Rather than inserting our import hook immediately upon execution
of this module, we put the code to do so in the function
``add_hook``, and return the hook that was created.
This has at least four benefits:

    1.  We can control when the hook is created.
    2.  We can use the return value to change some of its parameters,
        for example to temporarily disable it, or to remove it
        altogether. This can be particularly useful for testing.
    3.  We can optionally add arguments to ``add_hook``; we will do so
        in more complex examples
    4.  Perhaps the most import benefit is that, as we have seen before,
        we can invoke ideas from the command line with the
        ``-a`` or ``--add_hook`` flag,

        .. code-block:: none

            ideas --add_hook function_keyword

        which imports ``function_keyword`` and calls ``function_keyword.add_hook()``.

.. sidebar:: Tokens?

    Your Python code is a sequence of various operators
    (``+``, ``-``, ``:``, etc.), keywords, strings, etc.
    Each of these is an individual **token**.

Using ``token_utils``
~~~~~~~~~~~~~~~~~~~~~

To replace ``function`` by ``lambda`` only when it is meant to be
used as a keyword, we break up the code in a series of tokens
and only replace ``function`` by ``lambda`` when it occurs as
an individual token. Rather than using directly the module ``tokenize``
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
what changes have been made by the source transformation to the original script.


.. code-block:: none

    > ideas -a function_keyword my_program -s

    #========== Original source from docs_examples/usage/my_program.py ====
    # my_program.py

    square = function x: x**2
    print(f"{square(4)} is the square of 4.")

    if __name__ == '__main__':
        print(f"And the square of 5 is {square(5)}")
    #=== End of Original source from docs_examples/usage/my_program.py ====


    #========== Transformed source ====
    # my_program.py

    square = lambda x: x**2
    print(f"{square(4)} is the square of 4.")

    if __name__ == '__main__':
        print(f"And the square of 5 is {square(5)}")
    #=== End of Transformed source ====

    16 is the square of 4.
    And the square of 5 is 25


When using import hooks with a standard Python interpreter,
only modules that are imported are affected *as they are imported*.
Code that is entered later in the interpreter is left unchanged.
However, this is not the case for the |ideas| console.
In the |ideas| console, since we see the original source
(the code we wrote), only the changed source is shown.


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

.. tip::

    Try out ``ideas_state.help()`` to get an idea of what
    information might be available or modified via ``ideas_state``.


Complete argument list for ``transform_source``
------------------------------------------------

In the above example, we had some unspecified keywords arguments
passed to ``transform_source``.

The last time this documentation was updated, the list of possible
arguments could be found in the arguments of ``hook.transform_source``
which is inside the method ``source_transforms``.

.. literalinclude:: ../../src/ideas/session.py
    :pyobject: State.source_transforms

``filename`` can sometimes be the name of the |ideas| console.

When using IPython or Jupyter, only the ``source`` is passed back to ``transform_source``.
