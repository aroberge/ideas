Customizing your first import hook
====================================

.. admonition:: Summary

    This builds upon our previous example of allowing
    ``function`` to being equivalent to ``lambda``.

    This example demonstrates the use of passing back parameters
    to an import hook and some possible usage.

    `Source code <https://github.com/aroberge/ideas/blob/master/src/ideas/included/function_keyword.py>`_

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
equivalent the ``function_keyword`` example,
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


Verbose finder
~~~~~~~~~~~~~~~

Suppose you want to see information about names and paths of
files that are searched by your Finder: you can do this by adding
an extra parameter to ``add_hook`` and
``import_hook.create_hook`` as follows::

    def add_hook(verbose_finder=False, **_kwargs):

        return import_hook.create_hook(
            transform_source=transform_source,
            verbose_finder=verbose_finder,
        )

Here's a sample session from a different example, where the import hook
is looking for files with a custom extension;
we use the ``--verbose`` flag which could have been
shortened to ``-v``. Note that, when used at the command line,
``-v/--verbose`` also sets ``-s/--show_changes`` to ``True``.::

    > ideas -a french --verbose my_program
    Added hook ideas.included.french
    Looking for files with extensions:  ['.pyfr']
    The following paths will not be included in the search:
    PYTHON: c:\\users\\andre\\appdata\\local\\programs\\python\\python311\\lib
    SITE-PACKAGES: c:\\users\\andre\\github\\ideas\\venv-ideas3.11\\lib\\site-packages
    IDEAS: c:\\users\\andre\\github\\ideas\\src\\ideas
        Searching for docs_examples/function/my_program.pyfr
        Found: docs_examples/function/my_program.pyfr


    #========== Original source from docs_examples/function/my_program.pyfr ====
    # my_program.pyfr

    afficher("Bonjour !")
    #=== End of Original source from docs_examples/function/my_program.pyfr ====


    #========== Transformed source ====
    # my_program.pyfr

    print("Bonjour !")
    #=== End of Transformed source ====

    Bonjour !



The last file that was needed was ``unicodedata.py`` from the Python
standard library; it was found by a "normal" finder used by Python.


Comparing the original and the transformed source
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. sidebar:: pattern != actual code

    You don't need to implement this as there already
    exists something similar available within |ideas|.

    This examples demonstrates how to create your own version
    of ``callback_params``, if there isn't already something that
    you need available within |ideas|.

It might be sometimes useful to compare the original source with
the transformed one. Instead of actually adding ``print`` statements
when needed, we could use some callback parameters to enable or disable
such ``print`` statemeent.  |ideas| makes it fairly easy to
do this using callback parameters.
Here's the basic **pattern** used in almost all the examples::

    def transform_source(source, callback_params=None, **kwargs):
        if callback_params is not None:
            if callback_params["show_original"]:
                print(source)

        new_source = do_transform(source)

        if callback_params is not None:
            if callback_params["show_changes"]:
                print(new_source)
        return new_source


    def add_hook(show_original=False, show_changes=False):
        callback_params = {
            "show_original": show_original,
            "show_changes": show_changes,
        }
        hook = import_hook.create_hook(
            transform_source=transform_source,
            callback_params=callback_params,
        )
        return hook


Here's an actual example using one such parameter to show the transformed
source::

    >>> from ideas.included import function_keyword
    >>> hook = function.add_hook(show_changes=True)
    >>> from ideas import console
    >>> console.start()
    Configuration values for the console:
        callback_params: {'show_original': False, 'show_changes': True}
        transform_source from ideas.included.function
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

