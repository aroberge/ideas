Customizing your first import hook
====================================

.. admonition:: Summary

    This builds upon our previous example of allowing
    ``function`` to being equivalent to ``lambda``.

    This example demonstrates the use of passing back parameters
    to an import hook and some possible usage.

Building a more complete example
----------------------------------

In addition to making it easy to create import hooks, |ideas| also
attempts to make it easy to include diagnostic "tools".
The ``function_keyword`` example, whose API listed below includes
links to the actual source, includes such "tools".
While they can help during development, they do admitedly make
the code more complicated.  If you want to create your own hook,
you do not have to include all possible features.

For example, here is a much simpler version, functionally
equivalent the
`function_keyword included with ideas <https://github.com/aroberge/ideas/blob/master/src/ideas/included/function_keyword.py>`_
but without some diagnostic options included::

    from ideas import import_hook, token_utils

    def transform_source(source, **_kwargs):
        new_tokens = []
        for token in token_utils.tokenize(source):
            if token == "function":
                token.string = "lambda"
            new_tokens.append(token)
        return token_utils.untokenize(new_tokens)

    def add_hook(**_kwargs):
        return import_hook.create_hook(transform_source=transform_source, name=__name__)


Note the unused ``**_kwargs`` in the definition of ``transform_source``
and ``add_hook``:
you should ensure to add something similar when creating your own import hook
even if you do not plan to make use of extra parameters.
Also, each import hook should have a unique ``name``: by convention, we use the ``name``
of the module (``__name__``) where it is defined
and we never have two import hooks created in the same module.

Goal: comparing the transformed code with the original source
--------------------------------------------------------------

It might be sometimes useful to compare the original source with
the transformed one. Instead of actually adding ``print`` statements
when needed, we could use some callback parameters to enable or disable
such ``print`` statemeent.  |ideas| makes it fairly easy to
do this using callback parameters.
Here's the basic **pattern** used in almost all the examples:

.. include:: ../../docs_examples/first_hook_customized/my_function_keyword.py
   :code: python


Here's an actual example started from a standard Python interpreter
(which cannot tranform the code in the REPL itself),
and where we use the |ideas| console to only highlight the changes::

    >>> import my_function_keyword
    >>> my_function_keyword.add_hook()
    <Ideas import hook: my_function_keyword>
    >>> from ideas import console
    >>> console.start()
    Ideas Console version 0.3.3. [Python version: 3.11.9]
    ideas> sq = function x: x**2
    ideas> sq(3)
    9

.. admonition:: Console quirk

    Regardless of how you attempt to modify the source,
    the strings ``exit()`` and ``quit()`` are hard-coded in
    |ideas| **console** to do what a normal user would expect.
    We had to do this after the nice :doc:`polish_expr <included/polish_expr>` (Reverse
    Polish notation) import hook example was contributed
    by Devin J. Pohly and we attempted to use it. 😉