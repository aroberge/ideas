Implicit multiplication
=======================

.. admonition:: Summary

    Using a very simple transformation during the tokenzing phase,
    Python's syntax is extended to recognize that multiplication is implied
    in some situations that would normally be identified as ``SyntaxError``
    since a multiplication operator ``*`` would be considered
    to be missing.

    `Source code <https://github.com/aroberge/ideas/blob/master/ideas/examples/implicit_multiplication.py>`_


Algebra
-------

Let's talk about algebra.  Consider the following set of equations.

.. code-block:: none

    ax = 1
    ay = 2
    az = 3

    x1 = 2ax
    x2 = 3(ax + ay)
    x3 = ax ay
    x4 = (ax + ay)4
    x5 = (ax + ay)az
    x6 = ax(ay + az)


I am confident that you can calculate the values of the unknowns ``x1`` to
``x6``.

Now, suppose that the above would be code written as a Python program.
You would find that the lines for ``x1`` to ``x5`` would give rise
to ``SyntaxError``, whereas the last one would be a ``TypeError``.
Python's syntax could be change to allow the cases above that
result in a ``SyntaxError`` without breaking anyone's program.

Here is another equation, taken from a class I taught last week.

.. code-block:: none

    y = 2A cos(k x + (w_1 + w_2)t/2) cos((w_1 - w_2)t/2)

If I were to write this as part of a Python program, and using the recommended
way of writing spaces around operators, I would have to write
is as follows::

    y = 2 * A * cos(k * x + (w_1 + w_2) * t / 2) * cos((w_1 - w_2) * t / 2)

Which of the two do you find easier to decipher?  Personally, it is the first
one.


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
and what mathematicians would write, so that the equation I mentioned
and wrote as:

.. code-block:: none

    y = 2A cos(k x + (w_1 + w_2)t/2) cos((w_1 - w_2)t/2)

would be valid Python code?

This can be done with the ``implicit_multiplication`` import hook.


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
