Guide to the examples
======================

The examples included are listed roughly in increasing level of complexity.

Source transformations
----------------------

Improving function as a keyword
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This example should be your starting point.
We show how to use the tokenizer to transform a source and explain
how to make use of some diagnostic "tools". Admittedly, using
these "tools" make the code more complicated than strictly needed.
Since we incorporate such "tools" in later examples, you might want
to be familiar with them so that you can learn to recognize and potentially
ignore them while looking at the actual code.


nobreak as a keyword
~~~~~~~~~~~~~~~~~~~~~

This shows how to keep track of indentation
level and only replace a keyword when some conditions are met.

repeat as a keyword
~~~~~~~~~~~~~~~~~~~~

This includes four different transformations,
one of which requires to add some extra variables to the original code.
We do so in a way that avoid any conflict with existing variable names.

French Python
~~~~~~~~~~~~~

This is a source transformation that allows one
to use French equivalent keywords to the existing ones.
It shows how to make use of a different file extension (``.pyfr``)

French repeat
~~~~~~~~~~~~~~

Extends the French keywords from **French Python** to include those
in **repeat as a keyword**. It then combines both examples into
a single transformation.

Auto-self
~~~~~~~~~~~~~~

This is an example of a syntax that is intended to reduce
boilerplate code when initializing a class instance.
The code transformation is more complex than the previous ones and
include a change of indentation of an entire block of code.S

Fractional math (token)
~~~~~~~~~~~~~~~~~~~~~~~~

This is a functionally equivalent version to the AST proof of concept
example [Fractional math (ast)] mentioned below.
It demontrattes how to include
supplementary code, such as importing a module or defining a function,
in addition to the user code, while ensuring that the console (REPL)
can still work properly.


Abstract Syntax Tree transformations
------------------------------------

Fractional math (AST)
~~~~~~~~~~~~~~~~~~~~~~

This is a proof-of-concept of a transformation
at the Abstract Syntax Tree level. It also shows how to include
supplementary code, such as importing a module or defining a function,
in addition to the user code while ensuring that the console (REPL)
can still work properly.

Switch statement
~~~~~~~~~~~~~~~~~

Implementing a switch statement as described in the rejected PEP 3103.

Implicit multiplication
~~~~~~~~~~~~~~~~~~~~~~~~~

Python's syntax does not allow to write a number followed by an
non-keyword identifier or by a parenthesis, nor does it allow to write two
non-keyword identifiers in a row. However, when writing equations on
paper, these constructs are recognized as indicating a multiplication.
This transformation does the same.

Bytecode transformations
-------------------------

Confused math
~~~~~~~~~~~~~~~~~

This is a proof-of-concept bytecode transformation.

Other types
------------

True constants
~~~~~~~~~~~~~~~~~~

This is a fairly complex example that illustrates
the use of a custom module dict and class.

Custom encoding
---------------

Import hooks are not the only way one can transform a source; this
can also be done by custom encodings.

λ encoding
~~~~~~~~~~~~~~~

This is an adaptation of our basic example, but using a custom
encoding which needs to be explicitly declared in a file whose
source must be transformed.
