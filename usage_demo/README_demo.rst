Basic usage
-----------

Suppose that you want to use ``function`` as a keyword in Python, to mean
the same thing as ``lambda``, enabling you to write::

    # my_program.py

    square = function x: x**2
    print(f"{square(4)} is the square of 4.")

    if __name__ == '__main__':
        print(f"And the square of 5 is {square(5)}")


You could do this by creating the following program::

    # loader_1.py

    from ideas.examples import function_keyword
    function_keyword.add_hook()

    import my_program


and then run::

    python loader_1.py

The result will be::

    16 is the square of 4.



Another way to activate the hook is using either a sitecustomize.py file
(not recommended) or a temporary usercustomize.py file.  For example::

    # usercustomize.py

    from ideas.examples import function_keyword
    function_keyword.add_hook()

    print("  --> usercustomize.py was executed")


By setting the environment variable ``PYTHONPATH``, we can tell Python
to run this file first.  On Windows, this can be done as the following::

    set PYTHONPATH=%CD%

Once we have done this, if we use::

    # my_other_program.py

    import my_program

and run::

    python my_other_program.py

the result will be::

      --> usercustomize.py was executed
    16 is the square of 4.

So, we can see that our import hook has be set correctly by using
a usercustomize.py file. Unfortunately, if we attempt to do the
following, a ``SyntaxError`` will be raised::

    $ python my_program.py
      --> usercustomize.py was executed
      File "my_program.py", line 3
        square = function x: x**2
                          ^
    SyntaxError: invalid syntax

Python (cPython at least...) ignores the existence of any import hook
when executing the main script. Perhaps I should make a suggestion
to change this on Python-ideas. ;-)

.. todo::

    Implement make_encoding and add example.


Using the Ideas Console
-----------------------

If you can't write code in an REPL to try it out, then you are not
using Python. So, of course ``ideas`` has to include its own (likely buggy)
version of an interpreter.


We can activate it as follows::

    $ python
    Python 3.7.3 ...

    >>> from ideas.examples import function_keyword
    >>> hook = function_keyword.add_hook()
    >>> from ideas import console
    >>> console.start()
    Configuration values for the console:
        callback_params: {'show_original': False, 'show_transformed': False}
        transform_source from ideas.examples.function_keyword
    --------------------------------------------------
    Ideas Console version 0.0.4. [Python version: 3.7.3]

    ~>> cube = function x: x**3
    ~>> cube(3)
    27
    ~>>

Alternatively, using the ``-i`` option of the standard Python
interpreter with one of our previous examples, we do not have
to write code to add our hook as it is already set::

    $ python -i loader_1.py
    16 is the square of 4.
    >>>
    >>> from ideas import console
    >>> console.start()
    Configuration values for the console:
        callback_params: {'show_original': False, 'show_transformed': False}
        transform_source from ideas.examples.function_keyword
    --------------------------------------------------
    Ideas Console version 0.0.4. [Python version: 3.7.3]

    ~>> square = function x: x**2
    ~>> square(-5)
    25
    ~>>

