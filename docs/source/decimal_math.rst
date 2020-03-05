Decimal math
==============

.. admonition:: Summary

    Does decimal math automatically.

    Adds the required import of the the decimal module automatically.

    Can be used either as an import hook or as a custom codec.


    `Source code <https://github.com/aroberge/ideas/blob/master/ideas/examples/decimal_math.py>`_


.. warning::

    The following is just a quick first draft.


On Python-ideas, the `following question was recently asked <https://mail.python.org/archives/list/python-ideas@python.org/thread/7EF5MOJK5GOQZZEZXQ7DKM2N52JZ7VNB/>`_

    Wouldn't it be possible to have something along the lines of::

        from decimal import TreatFloatsAsDecimal
        @TreatFloatsAsDecimal
        a = 0.1  # These are all now decimals
        b = 0.2
        c = 0.3
        a + b == c # This now works


The answer is yes, using either an import hook or a custom encoding already
implemented as an example. Here we show it in action using a REPL::


    >>> from ideas.examples import decimal_math
    >>> hook = decimal_math.add_hook()
    >>> from ideas import console
    >>> console.start()
    Configuration values for the console:
        source_init from ideas.examples.decimal_math
        transform_source from ideas.examples.decimal_math
    --------------------------------------------------
    Ideas Console version 0.0.15. [Python version: 3.7.3]

    ~>> 0.1 + 0.2 == 0.3
    True
    ~>> 0.1 * 10 == 1
    True
    ~>> 0.1
    Decimal('0.1')
    ~>> 0.1 + 0.100
    Decimal('0.200')

.. warning::

    In the description below, setting ``PYTHONPATH`` in a terminal
    will only work as described
    if you install ideas in a normal (not virtual) environment.


Import hook
-------------

To use and test it easily as an import hook, you can do the following.

1. Create a file named ``usercustomize.py`` containing the following:

.. code-block:: python

    from ideas.examples import decimal_math
    decimal_math.add_hook()

2. Assuming you are not in virtual environment, set the ``PYTHONPATH``
   environment variable to the path where ``usercustomize.py`` is found.
   On Windows, this is most done by navigating where this file is found
   and typing: ``set PYTHONPATH=%cd%``

You can now invoke your module doing the following::

    python -c "import my_script"


Custom codec
-------------

To use and test it easily as a custom codec, you can do the following.

1. Create a file named ``usercustomize.py`` containing the following:

.. code-block:: python

    from ideas.examples import decimal_math
    decimal_math.register()

2. Assuming you are not in virtual environment, set the ``PYTHONPATH``
   environment variable to the path where ``usercustomize.py`` is found.
   On Windows, this is most done by navigating where this file is found
   and typing: ``set PYTHONPATH=%cd%``

3. At the top of the module you wish to be run with the special codec,
   add the following two lines::

        # coding: decimal-math
        from decimal import Decimal

You can now invoke your module doing the following::

    python my_script.py


.. automodule:: ideas.examples.decimal_math
   :members:
