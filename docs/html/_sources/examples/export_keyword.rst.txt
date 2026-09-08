.. admonition:: Summary

   This import hook makes ``export`` a soft keyword, so that it automatically adds to
   ``__all__`` the relevant names in the following cases::

      export class ClassName ...

      export def function_name ...

      export identifier ... = ...

   In a sense, it complements the ``pep_843`` import hook.

   `Source code <https://github.com/aroberge/ideas/blob/master/ideas/examples/export_keyword.py>`_

.. automodule:: ideas.examples.export_keyword
