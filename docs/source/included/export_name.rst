export name (PEP 842)
==================================

.. admonition:: Summary

   This import hook makes ``export`` a soft keyword, so that it automatically adds to
   ``__all__`` the relevant names in the following cases::

      export class ClassName ...

      export def function_name ...

      export name ... = ...

   where these statements occur at the top level (i.e. not within a function or class definition).
   In some sense, it complements the :doc:`from ... export (PEP 843) <./from_export>` import hook.
   In the next section, we demonstrate how we can combine these two import hooks.

   `Source code <https://github.com/aroberge/ideas/blob/master/src/ideas/included/export_name.py>`_

.. automodule:: ideas.included.export_name


We will see how to combine our limited implementation of both PEP 842 and PEP 843
in the next section, :doc:`export as a keyword <./export_keyword>`.