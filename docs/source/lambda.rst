λ encoding
==========

.. admonition:: Summary

    Using a custom codec instead of an import hook.


    `Source code <https://github.com/aroberge/ideas/blob/master/ideas/examples/lambda_encoding.py>`_


.. warning::

    The following is just a quick first draft.

Suppose we want to run a program that has a custom encoding;
in this case, we use ``λ`` to represent Python's ``lambda`` keyword::

    # coding: lambda-encoding

    square = λ x: x**2

    assert square(3) == 9

    print("Using lambda-encoding: λ")  # λ is not converted inside strings

    if __name__ == '__main__':
        print("The square of 5 is", square(5))

Before we can do this, we need to make Python aware of the existence
of our custom encoding. This can be done by having the following
program::

    # usercustomize.py

    from ideas.examples import lambda_encoding  # noqa

    print("  --> usercustomize.py was executed")


By setting ``PYTHONPATH`` to a directory where a program named
``usercustomize.py`` is found, any such program is automatically run before
the main script.

As we can see, when we run it, the source transformation is done
correctly.

.. code-block:: none

    TESTS:\lambda_encoding
    $ set PYTHONPATH=%CD%

    TESTS:\lambda_encoding
    $ python short_program.py
      --> usercustomize.py was executed
    Using lambda-encoding: λ
    The square of 5 is 25


We can also use the **ideas** console and have our special encoding be used.::

    >>> from ideas.examples import lambda_encoding
    >>> lambda_encoding.enable_console()
    >>> from ideas import console
    >>> console.start()
    Configuration values for the console:
        transform_source from ideas.examples.lambda_encoding
    --------------------------------------------------
    Ideas Console version 0.0.5. [Python version: 3.7.3]

    ~>> sq = λ x: x*x
    ~>> sq(3)
    9

.. automodule:: ideas.examples.lambda_encoding
   :members:
