.. important::

    The goal of |ideas| is to offer the possibility to
    easily experiment with alternatives
    to Python's normal syntax, exploring various "what if"
    scenarios.

export as a keyword (PEPs 842 + 843)
=====================================

.. admonition:: Summary

    We look at the effects of combining two import hooks to
    enable the use of the soft keyword ``export`` in 
    the following **top-level** statements::

        from module export A [[as B], ...]  # PEPs 842 and 843
        from module export *                # PEP 843 
        export name ... = ...               # PEP 842
        export def function_name():         # PEP 842
        export def class ClassName:         # PEP 842

    The two import hooks we use here are separately described
    in :doc:`export name (PEP 842) <./export_name>` and 
    :doc:`from ... export (PEP 843) <./from_export>`.


`PEP 842 (withdrawn) <https://peps.python.org/pep-0842/>`_ and
`PEP 843 <https://peps.python.org/pep-0843/>`_
are two "competing" PEPs which propose the addition of 
``export`` as a *soft* keyword. [1]_


Before showing how to combine both import hooks included in |ideas|
to demonstrate this use of ``export`` as a soft keyword,
we offer this *subjective* summary of the advantages of 
introducing this change to Python's syntax.

+ For people **writing** modules, being able to use ``export``
  as a keyword avoid having to write the same name twice,
  both where a declaration or import statement occur and 
  in adding it to ``__all__`` by hand. By avoiding this 
  duplication, the possibility of errors caused by 
  forgetting to keep ``__all__`` in sync is reduced.

+ For people **reading** source code, expecially for large 
  modules, the use of ``export``
  would make it much easier to identify names that 
  are intended to be part of the public interface as 
  they are reading the code, without having to 
  look for a definition of ``__all__``.

* Having an ``export`` keyword might make it possible to 
  avoid writing code such as::

    from module import Name as Name 
  
  just to satisfy linters.

+ As mentioned in `PEP 843 <https://peps.python.org/pep-0843/>`_,
  the use of ``from ... export ...`` would make it easier 
  for people writing large packages using a "hub model"
  to maintain a stable public API while making internal
  changes.

+ Using ``export`` in all the cases mentioned above rather than 
  using a **combination** of ``from ... export ...`` and the 
  ``@public`` package (see `PEP 844 <https://peps.python.org/pep-0844/>`_)
  would be more aesthetically pleasing. [2]_

Example
--------

When exploring a script interactively with Python, one uses::

    py -i script.py

To explore a package, one needs to import it, which is essentially
as easy to start::

    > py
    Python 3.11.9
    >>> import package

As we have seen before, using both import hooks, namely 
:doc:`export name (PEP 842) <./export_name>` and 
:doc:`from ... export (PEP 843) <./from_export>`, 
within a standard Python REPL
would require typing many more statements to set things
up before starting exploring the content of a package.
Instead, I will use the |ideas| console. 
I will do so to explore use the following **very contrived package**
essentially demonstrating the use of all cases of ``export``.

The package structure is as follows:

.. code-block:: none

    export_hub/
         __init__.py
         gadgets.py
         utils.py
         sub_hub/
             __init__.py
             abc_s.py

.. code-block::

    # export_hub/__init__.py

    from export_hub.gadgets export Widget, Gadget as NewGadget

    from export_hub.utils export useful

    from export_hub.sub_hub.abc_s export a, b, c

.. code-block::

    # export_hub/gadgets.py

    class Widget: pass

    class Gadget: pass

    class NotWidget: pass

    class NotGadget: pass

.. code-block::

    # export_hub/utils.py
    import inspect


    export def pdir(obj=None):  # currently meant for internal use by the Team.
        """Returns the contents of ``__all__`` if available,
        if not returns what ``dir`` would."""
        

        if obj is not None:
            if hasattr(obj, "__all__"):
                return obj.__all__
            return dir(obj)

        caller_frame = inspect.currentframe().f_back
        caller_locals = caller_frame.f_locals if caller_frame else {}
        if obj is None:
            if "__all__" in caller_locals:
                return caller_locals["__all__"]
            else:
                return list(caller_locals)  # only the keys

    export def useful(): print("I'm useful.")

    def internal(): pass

.. code-block::

    # export_hub/sub_hub/abc_s.py

    a = b = c = d = e = f = ...


Let's proceed with the |ideas| console, adding two 
source transformations (using the ``-a`` flag) and continuing
in interactive mode (``-i``) to import a module and 
proceed to examine its content.

.. code-block::

    > ideas -i -a from_export -a export_name export_hub
    Ideas Console version 0.2.0. [Python version: 3.11.9]
    ideas> dir()
    ['NewGadget', 'Widget', '__all__', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__path__', '__spec__', 'a', 'b', 'c', 'ideas_state', 'gadgets', 'sub_hub', 'useful', 'utils']

Note that ``ideas_state`` is an object that is always present in 
the |ideas| console and allows one to change various parameters,
something we will not need to do here.

I notice the name ``utils``, which suggests that it might be useful to look at it.

.. code-block::

    ideas> utils
    <module 'export_hub.utils' from 'C:\\Users\\Andre\\github\\ideas\\docs_examples\\export_hub\\utils.py'>
    ideas> dir(utils)
    ['__all__', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'inspect', 'internal', 'pdir', 'useful']

.. sidebar:: Reminder

    This is a very contrived example done for illustration and
    inspiration if you wished to set up your own examples,
    perhaps by copying an existing package, inserting ``export``
    in various places, and looking at the effect.
    

``utils`` seems to define a public interface as it contains ``__all__``. Let's import it.

.. code-block::

    ideas> from export_hub import utils
    ideas> utils.__all__
    ['pdir', 'useful']

Imagine that we found many more seemingly useful public functions, like ``pdir``,
not having been imported when first imported the main package. We could import them
now and try to make use of them.

.. code-block::

    ideas> from export_hub.utils import *  # excessive here
    ideas> help(pdir)
    Help on function pdir in module export_hub.utils:

    pdir(obj=None)
        Returns the contents of ``__all__`` if available,
        if not returns what ``dir`` would.

    ideas> pdir(utils)
    ['pdir', 'useful']
    ideas> pdir()
    ['Widget', 'NewGadget', 'useful', 'a', 'b', 'c']

.. tip::

    IPython/Jupyter users: As I am updating the documentation,
    I have not updated |ideas| to make sure that multiple
    transformations could be combined in those environment.
    Please file an issue if this affects you and I will try to 
    give it priority.


Last words
----------

If you have come here from 
`Python discuss <https://discuss.python.org/t/pep-843-export-statement-for-dry-re-exports/108687>`_,
and have tried the import hook(s), I hope that it has been useful in 
assessing whether or not having ``export`` as such a soft export keyword would be 
useful.

For those wishing to use |ideas| to **write** their own import hooks and use them
with the provided console, note that these the two import hooks used here 
are (so far) unique in that they transform single line statements into 
multiple line ones, as they add information about updating ``__all__``.
If your import hook does similar source code transformations,
these two examples contain the required information.


.. [1] A soft keyword is a name which is recognized as a Python keyword
       only in specific situations, but can otherwise be used as an 
       identifier such as a variable name, function name, etc.

.. [2] I did mention that this was a subjective opinion.