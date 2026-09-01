λ encoding
==========

.. admonition:: Summary

    This shows the result of using a custom codec instead of an import hook.
    It is only included as a proof of concept, as it is not as versatile
    as the import hooks.

Suppose we want to run a program that has a custom encoding:
this is done in Python by inserting a special ``coding`` directive
as the first line of our program.
In this simple example as proof of concept,
we use ``λ`` to represent Python's ``lambda`` keyword::

    # coding: lambda_encoding

    square = λ x: x**2

    assert square(3) == 9

    print("Using lambda-encoding: λ")  # λ is not converted inside strings
    print("The square of 5 is", square(5))

The basic code required create the ``lambda_encoding`` codec, reading
and decoding the file, is found in
`lambda_codec.py <https://github.com/aroberge/ideas/blob/master/ideas/examples/lambda_codec.py>`_

Before running our program with a custom encoding,
we need to make Python aware of the existence
of that encoding. Here is how we do it in the included
test files, usually run by pytest::

    # test_lambda_encoding.py
    # The following import will automatically register a codec
    from ideas.examples import lambda_codec  # noqa

    def test_import():
        from . import short_program  # noqa

    if __name__ == "__main__":
        import short_program


And here is the result:

.. code-block:: text

    (venv-ideas3.11) C:\Users\Andre\github\ideas
    > py tests/lambda_encoding/test_lambda_encoding.py
    lambda_encoding has been registered.
    Using lambda-encoding: λ
    The square of 5 is 25

.. warning::

    At this time, the **ideas** console cannot handle at the same time regular import hooks
    that are used to transform a source **and** transformations done using
    a custom codec: you can only use one or the other.

We can also use the **ideas** console and have our special encoding be used.::

    (venv-ideas3.11) C:\Users\Andre\github\ideas
    > py
    Python 3.11.9 ...

    >>> from ideas.examples import lambda_codec
    lambda_encoding has been registered.
    >>> from ideas import console
    >>> console.start()
    Ideas Console version 0.2.0. [Python version: 3.11.9]
    ideas> sq = λ x: x*x
    ideas> sq(3)
    9
    ideas>
