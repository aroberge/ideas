True constants
==============

**Summary:** How to ensure that variables defined as constants by some notational
convention are guaranteed not to change, without requiring them
to be attribute of an object.

This example demonstrates the use of:

- Source transformation to extract information from the source without changing its content.
- Custom module class
- Specialized dict to temporarily replace the read-only module dict.

It took me quite a while to come up with the solution described below,
and I learned a fair bit along the way.  Given the relative complexity of
the final solution, I thought it would be appropriate to start slowly,
explaining what is usually done by Pythonistas.

Consenting adults
-----------------

Unlike some other programming languages that force their users
to do things in a very strict fashion,
Python gives a lot of flexibility and assume that they are responsible adults,
capable of using common sense in their use of the language.
Thus, certain features considered to be absolutely essential in other languages,
such as keeping some variables hidden,
or forcing other variables to never have their type and sometimes not even their value changed once assigned, are not present in Python.
Instead, Pythonistas rely on conventions to indicate their intent.

- You want to indicate that a variable should be considered "private"? Just use a name starting with an underscore to communicate this to another programmer.

    - If that is not strong enough, use a double underscore to start its name. Other Python programmers will know what you mean.

- You want to indicate that a variable should be constant? Just write its name in UPPERCASE_LETTERS.

  - For Python 3.8, use a ``Final`` qualifier type hint as per `PEP 591 <https://www.python.org/dev/peps/pep-0591/>`_

Still, this does not prevent people from asking *"How do I create a constant in Python?"*
such as `was asked on StackOverflow <https://stackoverflow.com/questions/2682745/how-do-i-create-a-constant-in-python>`_
some 9 years ago, which has resulted in 34 different answers so far,
all of which indicate that you cannot enforce this convention in Python at a module level.
Answers that were provided are still actively edited as new features get added to Python,
including recent comments about using the ``Final`` qualifier.

While it is noted that you can use tools such as `mypy <http://mypy-lang.org/>`_
**only to check** without running the program
that a variable meant to be used as a constant is not expected to change,
all the other answers rely, in one way or another, on creating an object,
which can be **another** module,
and have the would-be constants defined as attribute to that object.
Such objects are carefully designed with properties that prevent
changes to the values of attributes intended to be constants.

However, this type of solution is more cumbersome to use than being able to simply
use an agreed-upon convention.
As Raymond Hettinger often says: **there must be a better way**. ;-)

How to
------

.. todo::

   Explain how to use this module

How does it work
----------------

.. todo::

    Explain how it works

Suggestion for you
------------------

Try to implement your own variation, perhaps by introducing ``let``
as a new keyword::

    let this_variable = 3  # this_variable is thus declared as constant

