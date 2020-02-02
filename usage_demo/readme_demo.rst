Basic usage
-----------

.. note:: If you don't like typing ...

    All the programs mentioned below are found in the ``usage_demo``
    directory in the code repository.

Suppose that you want to use ``function`` as a keyword in Python, to mean
the same thing as ``lambda``, enabling you to write::

    # my_program.py

    square = function x: x**2
    print(f"{square(4)} is the square of 4.")

    if __name__ == '__main__':
        print(f"And the square of 5 is {square(5)}")


You could do this by creating the following program::

    # loader_1.py

    from ideas.examples import function
    function.add_hook()

    import my_program


and then run::

    python loader_1.py

The result will be::

    16 is the square of 4.

Note that, perhaps unfortunately, ``my_program`` can not be run
as the main module.  This can be corrected by using::

    # loader_2.py

    from ideas.import_hook import import_as_main
    from ideas.examples import function
    function.add_hook()

    import_as_main("my_program")  # to be implemented


The result is::

    ...
    NotImplementedError

Another way to activate the hook is using either a sitecustomize.py file
(not recommended) or a temporary usercustomize.py file.  For example::

    # usercustomize.py

    from ideas.examples import function
    function.add_hook()

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

Using the IdeasConsole
----------------------

One of Python's very useful is the interactive interpreter.
``ideas`` includes its own version.

We can activate it as follows::

    $ python
    Python 3.7.3 (v3.7.3....
    >>> from ideas.examples import function
    >>> hook = function.add_hook()
    >>> from ideas import console
    >>> console.start()
    Configuration values for the console:
        transform_source: <function transform_source at 0x03933588>
        callback_params: {'show_original': False, 'show_transformed': False}
    --------------------------------------------------
    Ideas Console version 0.0.3. [Python version: 3.7.3]

    ~>> cube = function x: x**3
    ~>> cube(3)
    27
    ~>>

Alternatively, using the ``-i`` option of the standard Python
interpreter with one of our previous examples, we do not have
to write code to add our hook as it is already set::

    $ python -i loader_1.py
    16 is the square of 4.
    >>> from ideas import console
    >>> console.start()
    Configuration values for the console:
        transform_source: <function transform_source at 0x03CB4588>
        callback_params: {'show_original': False, 'show_transformed': False}
    --------------------------------------------------
    Ideas Console version 0.0.3. [Python version: 3.7.3]

    ~>> square = function x: x**2
    ~>> square(4)
    16
    ~>>

.. todo::

    Add name of the hook as part of the configuration values.
