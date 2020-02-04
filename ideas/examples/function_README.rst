.. To avoid duplication, this is used both as a readme file for the
   function_simplest.py module and as contents of the documentation.

Function - part 2
==================

**Summary:** This builds upon our previous example of allowing
``function`` to being equivalent to ``lambda``.

This example demonstrates the use of:

- Passing back parameters to an import hook and some possible usage.


Actual source
--------------

Here's the content of our example.

.. literalinclude:: ../../ideas/examples/function.py
   :emphasize-lines: 14-18,21,32-33,37-38,61
   :linenos:

On lines 14 to 18, we defined a function that can be used to print
either the original code or the transformed one.
This can be useful in debugging sessions. Once it has been written,
there is essential no advantage in removing the code: we leave it
in so that other programmers wishing to build upon this example
do not have to rewrite such code.

Whether or not we invoke the diagnostic code is determined
on lines 32-33, and 37-38.  The values of the relevant parameters
are actually set when we call the function to add a hook on
line 61.

In addition to these callback parameters, you might have noticed
on line 21 the extra function argument ``**kwargs``.
In addition to some parameters unique to each import hook,
our import hook machinery returns some other parameters, such
as the file name and others, which can be of use to some
transformers.  As a rule, every function that can be called
by the import hook machinery should include such an
unspecified argument.

