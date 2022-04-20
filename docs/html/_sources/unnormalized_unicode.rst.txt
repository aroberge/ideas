Unnormalized unicode
=====================

.. epigraph::

    *The idea for this example came from Sergey B. Kirpichev, who also
    wrote the first implementation.*


Consider the following examples from Julia's repl.

.. code-block:: julia

    julia> ℕ = 1
    1

    julia> N = 2
    2

    julia> N, ℕ
    (2, 1)

Let's attempt to do the same thing with Python::

    >>> ℕ = 1
    >>> N = 2
    >>> N, ℕ
    (2, 2)

Clearly, something is very different between these two programming
environments, both used heavily by scientists. It is possible to make
Python's output look similar to that of Julian.

.. code-block:: none

    > python -m ideas -a unnormalized_unicode
       The following initializing code from ideas is included:

    true_dir = dir
    from ideas.examples.unnormalized_unicode import new_dir as dir

    Ideas Console version 0.0.34. [Python version: 3.8.10]

.. code-block::

    >>> ℕ = 1
    >>> N = 2
    >>> N, ℕ
    (2, 1)

To understand why Python normally consider ``ℕ`` and ``N`` to be the
same requires more knowledge about unicode than what is found in a typical
tutorial.  But before we take a deeper dive into unicode land, let's
take a detour and talk about Julia.


More to come...
----------------

