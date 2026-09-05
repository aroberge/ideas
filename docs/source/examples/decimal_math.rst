Decimal math
==============

On Python-ideas, the `following question was recently asked <https://mail.python.org/archives/list/python-ideas@python.org/thread/7EF5MOJK5GOQZZEZXQ7DKM2N52JZ7VNB/>`_

    Wouldn't it be possible to have something along the lines of::

        from decimal import TreatFloatsAsDecimal
        @TreatFloatsAsDecimal
        a = 0.1  # These are all now decimals
        b = 0.2
        c = 0.3
        a + b == c # This now works


The answer is yes, using either an import hook or a custom encoding already
implemented as an example. Here we show it in action using the ideas repl:
`Source code for decimal_math <https://github.com/aroberge/ideas/blob/master/ideas/examples/decimal_math.py>`_

.. code-block:: none
    
    > py -m ideas -a decimal_math
        The following initializing code from ideas is included:

    from decimal import Decimal

    Ideas Console version 0.2.0. [Python version: 3.11.9]
    ideas> 0.1 + 0.2 == 0.3
    True
    ideas> 0.1 * 10 == 1
    True
    ideas> 0.1
    Decimal('0.1')
    ideas> 0.1 + 0.100
    Decimal('0.200')

There is a second version of decimal math, whith requires a ``D`` suffix after a 
float to transform it into a python Decimal.:
`Source code for decimal_math_d <https://github.com/aroberge/ideas/blob/master/ideas/examples/decimal_math_d.py>`_

.. code-block:: none
    
    > py -m ideas -a decimal_math_d
        The following initializing code from ideas is included:

    from decimal import Decimal

    Ideas Console version 0.2.0. [Python version: 3.11.9]
    ideas> 0.1 + 0.2
    0.30000000000000004
    ideas> 0.1D + 0.2D
    Decimal('0.3')

There is actually a third version of decimal math:
`Source code for decimal_math_with <https://github.com/aroberge/ideas/blob/master/ideas/examples/decimal_math_with.py>`_


.. code-block:: none

    > py -m ideas -a decimal_math_with
        The following initializing code from ideas is included:

    from decimal import Decimal

    Ideas Console version 0.2.0. [Python version: 3.11.9]
    ideas> with float_as_decimal:
    ...     a = 1.0
    ...     b = 2.0
    ...
    Traceback (most recent call last):
    File "*Ideas Console*", line 1, in <module>
    NameError: name 'float_as_decimal' is not defined
    ideas> with float_as_Decimal:
    ...     a = 1.0
    ...     b = 2.0
    ...
    ideas> a, b
    (Decimal('1.0'), Decimal('2.0'))
    ideas> c = 3.0
    ideas> c
    3.0
    ideas> a, b, c
    (Decimal('1.0'), Decimal('2.0'), 3.0)



.. automodule:: ideas.examples.decimal_math

.. automodule:: ideas.examples.decimal_math_d

.. automodule:: ideas.examples.decimal_math_with
