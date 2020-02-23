Guide to the examples
======================

The examples included are listed roughly in increasing level of
complexity.

**Improving function as a keyword** should be your starting point.
We show how to use the tokenizer to transform a source and explain
how to make use of some diagnostic "tools". Admittedly, using
these "tools" make the code more complicated than strictly needed.
Since we incorporate such "tools" in later examples, you might want
to be familiar with them so that you can learn to recognize and potentially
ignore them while looking at the actual code.

**nobreak as a keyword** shows how to keep track of indentation
level and only replace a keyword when some conditions are met.

**repeat as a keyword** includes four different transformations,
one of which requires to add some extra variables to the original code.
We do so in a way that avoid any conflict with existing variable names.

**French Python** is a source transformation that allows one
to use French equivalent keywords to the existing ones.
It is included mostly for historical reason.

**Auto-self** is an example of a syntax that is intended to reduce
boiler-plate code when initializing a class instance.
The code transformation is more complex than the previous ones and
include a change of indentation of an entire block of code.

All of the previous examples are done as source transformation.
However, we can do other types of transformations.

**Fractional math** is a proof-of-concept of a transformation
at the Abstract Syntax Tree level.

**Confused math** is a proof-of-concept bytecode transformation.

**True constants** is a fairly complex example that illustrates
the use of a custom module dict and class.

Finally, import hooks are not the only way one can transform a source; this
can also be done by custom codecs as demonstrated in
**λ encoding**.
