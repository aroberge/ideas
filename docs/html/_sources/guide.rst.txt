Guide to the examples
======================

The examples included are listed roughly in increasing level of complexity.
Source transformations and AST transformations can be used interactively
in IPython/Jupyter environments;  bytecode transformations and custom
encoding cannot.

.. sidebar:: Contribute!

    Feel free to contribute your own examples. However, note that,
    for safety reasons, I will not accept examples that result in 
    importing arbitrary code/modules from the Internet, as demonstrated
    in one of David Beazley's talks.


Source transformations
----------------------

Source transformations represent one of the easiest way to 
introduce new experimental syntax in Python. 
If you want to write your own import hook, it might be worth your while
reading a few of the following examples, if not all of them,
especially including examining the source code.

.. toctree::
    :maxdepth: 1

    nobreak as a keyword <examples/nobreak>
    repeat as a keyword <examples/repeat>
    French Python <examples/french>
    French repeat <examples/french_repeat>
    Auto-self <examples/auto_self>
    Decimal math <examples/decimal_math>
    Fractional math (token) <examples/fractional_math_tok>
    Switch statement <examples/switch>
    Implicit multiplication <examples/implicit_multiplication>
    Unnormalized unicode <examples/unnormalized_unicode>

Custom parsing
--------------

.. toctree::
    :maxdepth: 1

    Polish expressions <examples/polish_expr>

AST transformations
-------------------

.. toctree::
   :maxdepth: 1

    Fractional math (AST) <examples/fractional_math_ast>

Bytecode transformations
------------------------

.. toctree::
   :maxdepth: 1

    Confused math (Bytecode) <examples/bytecode>

More complex examples
---------------------

.. toctree::
   :maxdepth: 2

    True constants <examples/constants>

Custom encoding
---------------

Import hooks are not the only way one can transform a source; this
can also be done by custom encodings.

.. toctree::
   :maxdepth: 1

    Create your own codec <examples/lambda>

