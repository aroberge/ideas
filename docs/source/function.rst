Improving function as a keyword
================================

.. admonition:: Summary

    This builds upon our previous example of allowing
    ``function`` to being equivalent to ``lambda``.

    This example demonstrates the use of passing back parameters
    to an import hook and some possible usage.

    `Source code <https://github.com/aroberge/ideas/blob/master/ideas/examples/function_keyword.py>`_

Basic usage::

    from ideas.examples import function_keyword
    function_keyword.add_hook()

    import my_program


Building a complete example
----------------------------

In addition to making it easy to create import hooks, **ideas** also
attempts to make it easy to include diagnostic "tools".
The ``function_keyword`` example, whose API listed below includes
links to the actual source, includes such "tools".
While they can help during development, they do admitedly make
the code more complicated.  If you want to create your own hook,
you do not have to include all possible features.

For example, here is a much simpler version, functionally
equivalent the ``function_keyword`` example,
but without some diagnostic options included::


    from ideas import import_hook, token_utils

    def transform_source(source, **kwargs):
        new_tokens = []
        for token in token_utils.tokenize(source):
            if token == "function":
                token.string = "lambda"
            new_tokens.append(token)
        return token_utils.untokenize(new_tokens)


    def add_hook():
        return import_hook.create_hook(transform_source=transform_source)


Note the unused ``**kwargs`` in the definition of ``transform_source``:
you should ensure to add something similar when creating your own import hook
even if you do not plan to make use of extra parameters.


Verbose finder
~~~~~~~~~~~~~~~

Suppose you want to see information about names and paths of
files that are searched by your Finder: you can do this by adding
an extra parameter to ``add_hook`` and
``import_hook.create_hook`` as follows::

    def add_hook(verbose_finder=False):

        return import_hook.create_hook(
            transform_source=transform_source,
            verbose_finder=verbose_finder,
        )

Here's a sample session from a different example, where the import hook
is looking for files with a custom extension::

    >>> from ideas.examples import french
    >>> hook = french.add_hook(verbose_finder=True)
    Looking for files with extensions:  ['.pyfr']
    The following paths will not be included in the search:
       PYTHON: == c:\users\andre\appdata\local\programs\python\python37-32\lib
       IDEAS: == c:\users\andre\github\ideas\ideas
    >>> import mon_programme
        Searching for TESTS:\french\mon_programme.pyfr.
    ->  Found:  TESTS:\french\mon_programme.pyfr

        Searching for TESTS:\french\unicodedata.pyfr.
      IdeasMetaFinder did not find unicodedata.

The last file that was needed was ``unicodedata.py`` from the Python
standard library; it was found by a "normal" finder used by Python.


Comparing the original and the transformed source
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. sidebar:: pattern != actual code

    The code used is slightly different than was is shown here.

It might be sometimes useful to compare the original source with
the transformed one. Instead of actually adding ``print`` statements
when needed, we can use some callback parameters to enable or disable
such ``print`` statemeent.  **ideas** makes it fairly easy to
do this using callback parameters.
Here's the basic **pattern** used in almost all the examples::

    def transform_source(source, callback_params=None, **kwargs):
        if callback_params is not None:
            if callback_params["show_original"]:
                print(source)

        new_source = do_transform(source)

        if callback_params is not None:
            if callback_params["show_transformed"]:
                print(new_source)
        return new_source


    def add_hook(show_original=False, show_transformed=False):
        callback_params = {
            "show_original": show_original,
            "show_transformed": show_transformed,
        }
        hook = import_hook.create_hook(
            transform_source=transform_source,
            callback_params=callback_params,
        )
        return hook


Here's an actual example using one such parameter to show the transformed
source::

    >>> from ideas.examples import function_keyword
    >>> hook = function.add_hook(show_transformed=True)
    >>> from ideas import console
    >>> console.start()
    Configuration values for the console:
        callback_params: {'show_original': False, 'show_transformed': True}
        transform_source from ideas.examples.function
    --------------------------------------------------
    Ideas Console version 0.0.4. [Python version: 3.7.3]

    ~>> square = function x: x**2
    ===========Transformed============
    square = lambda x: x**2
    -----------------------------
    ~>> square(3)
    ===========Transformed============
    square(3)
    -----------------------------
    9
    ~>>


.. tip::

    You do not need to make use of these extra features when
    creating your own hooks.

If you want to have a look at the actual source for ``function_keyword``,
use the links below.

.. sidebar:: API

    Generated by Sphinx

.. automodule:: ideas.examples.function_keyword
   :members:
