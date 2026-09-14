export as a keyword (PEPs 842 + 843)
=====================================

See :doc:`export name (PEP 842) <./export_name>` and 
:doc:`from ... export (PEP 843) <./from_export>` for more details.


The result of using this soft keyword is to automatically
add the name of the object to ``__all__``.

An additional option that we included, also inspired by
PEP 842, is the possibility to automatically define a custom
``__dir__`` which would result in only the "exported"
identifiers to be visible within an REPL.

This import hook complements well and can easily be combined
the pep_843 import hook described in a previous section.

.. important::

    The goal of **ideas** is to offer the possibility to
    easily experiment with alternatives
    to Python's normal syntax, exploring various "what if"
    scenarios.

    Unusually for this project, since two related examples
    are inspired by actual proposed PEPs, we give a
    **highly subjective** evaluation of what the proposed
    syntax would achieve.

Combining the import hooks export_name and pep_843
would result in the following:

    1. Reduce the work required in creating a public interface
       by adding names to ``__all__`` by hand while reducing
       the possibility of errors.
    2. Enabling anyone reading source code to easily identify
       which names are meant to be part of the public
       interface.
    3. Enable developers to easily change names in their
       various subdirectories while maintaining a stable
       public API.
    4. With the inclusion of a an optional custom ``__dir__``
       as described below, enable programmers to use a REPL
       to explore the various files of a project and, know
       which names can likely be safely used as they have
       been declared to be "public" via an ``export``
       statement.

There is perhaps a better alternative to item 4 above, as I
will describe below.


First example: export keyword only
-----------------------------------

Consider the following case::

    # sample_file.py

    from math import pi

    export PI = pi

    export public = "public variable"

    export def useful_fn():
        print("This is a very useful function")

    def private():
        print("I want to be able to change my name.")

    secret = "Ideas's code is a mess."

We will import and explore the content of this file in two
different sessions. First, with the default Python ``dir``.

.. code-block::

    >>> from ideas.included.export_name import add_hook
    >>> hook = add_hook()
    >>> # Let's first see what's already here
    >>> dir()
    ['__annotations__', '__builtins__', '__doc__', '__loader__', '__name__', '__package__', '__spec__', 'add_hook', 'hook']
    >>> __name__
    '__main__'
    >>> # Let's import a sample file
    >>> import sample_file
    >>> dir(sample_file)
    ['PI', '__all__', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'pi', 'private', 'public', 'secret', 'useful_fn']
    >>> sample_file.__name__
    'sample_file'
    >>> # We see many names; let's import "everything"
    >>> from sample_file import *
    >>> dir()
    ['PI', '__annotations__', '__builtins__', '__doc__', '__loader__', '__name__', '__package__', '__spec__', 'add_hook', 'hook', 'public', 'sample_file', 'useful_fn']
    >>> # We did not import pi, private and secret. Did anything else change?
    >>> __name__
    '__main__'
    >>> # Python does the right thing when it comes to dunders ...

Let's try again, using the ``public_dir`` option.

.. code-block::

    >>> from ideas.included.export_name import add_hook
    >>> hook = add_hook(public_dir=True)  # optional argument
    >>> import sample_file
    >>> dir(sample_file)
    ['PI', 'public', 'useful_fn']
    >>> # much cleaner; let's import everything
    >>> from sample_file import *
    >>> dir()
    ['PI', '__annotations__', '__builtins__', '__doc__', '__loader__', '__name__', '__package__', '__spec__', 'add_hook', 'hook', 'public', 'sample_file', 'useful_fn']
    >>> sample_file.secret
    "Ideas's code is a mess."
    >>> # Even though it was hidden, the secret is not safe if you are determined enough

    
.. tip::

    IPython/Jupyter users: I have not updated Ideas to make sure that multiple
    transformations could be combined in those environment. Please file an issue
    if this affects you.
