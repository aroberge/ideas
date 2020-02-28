Implicit multiplication
=======================

.. admonition:: Summary

    Using a very simple transformation during the tokenzing phase,
    Python's syntax is extended to recognize that multiplication is implied
    in some situations that would normally be identified as ``SyntaxError``
    since a multiplication operator ``*`` would be considered
    to be missing.

    `Source code <https://github.com/aroberge/ideas/blob/master/ideas/examples/implicit_multiplication.py>`_


Quoting from a `post from Guido van Rossum <https://mail.python.org/archives/list/python-ideas@python.org/message/52DLME5DKNZYFEETCTRENRNKWJ2B4DD5/>`_:

    *The power of visual processing really becomes apparent when you combine
    multiple operators. For example, consider the distributive law*::

        mul(n, add(x, y)) == add(mul(n, x), mul(n, y))  (5)

    *That was painful to write, and I believe that at first you won't see the
    pattern (or at least you wouldn't have immediately seen it if I hadn't
    mentioned this was the distributive law).*
    *Compare to*::

        n * (x + y) == n * x + n * y    (5a)

    *Notice how this also uses relative operator priorities. Often
    mathematicians write this even more compact*::

        n(x+y) == nx + ny    (5b)

    *but alas, that currently goes beyond the capacities of Python's parser.*
    ...
    *Now, programming isn't exactly the same activity as math, but we all know
    that Readability Counts, and this is where operator overloading in Python
    comes in*.  ...


What if we could do something half-way between what Python currently allow
and what mathematicians would write?

.. code-block:: python

    >>> from ideas.examples import implicit_multiplication as mul
    >>> hook = mul.add_hook()
    >>> from ideas import console
    >>> console.start()
    Configuration values for the console:
        callback_params: {'show_original': False, 'show_transformed': False}
        transform_source from ideas.examples.implicit_multiplication
    --------------------------------------------------
    Ideas Console version 0.0.7a. [Python version: 3.7.3]

    ~>> 2(3 + 4)
    14
    ~>> a = 3
    ~>> b = 4
    ~>> 2a
    6
    ~>> a b
    12

.. automodule:: ideas.examples.implicit_multiplication
   :members:
