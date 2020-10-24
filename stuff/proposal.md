# Experimental Syntax Proposal

I would like to propose that Python adopts a modified process
before introducing significant changes of its syntax.

## Preamble

Given the following file:

```python
# coding: experimental-syntax

from experimental-syntax import fraction_literal
from experimental-syntax import decimal_literal

assert 1 /3F == Fraction(1, 3)
assert 0.33D == Decimal('0.33')

print("simple_test.py ran successfully.")
```

This is what happens when I run it, with the standard Python interpreter:
```
$ python simple_test.py
simple_test.py ran successfully.
```

In what follows, I use this as a concrete example for one
of the three possible options mentioned.


## The problem

Python evolves in many ways including with the addition
of new modules in the standard libray and
with the introduction of new syntax.

Before considering the addition of a module in
the standard library, it is often suggested to have a
version on Pypi so that users can experiment with it,
which can lead to significant improvements.

However, when it comes to proposed syntax changes,
this is currently not possible to do, at least not in any
standard way that would easily be recognized by the wider community.


## Proposed solutions

For those that agree that this is something that could be
improved upon, I see at least three possible solutions.

1. Adoption of a simple convention to identify the use of non-standard syntax.
   This could take the form of a comment with a specific form
   introduced near the top of the file.  This comment could be used as
   a search term, to identify modules or projects that make use of
   some custom syntax.

2. Addition of a special encoding module in the Python standard library
   that can be used to implement nonstandard syntax through source
   transformation. The short program written at the top provides an
   example of what this might look like. Note the comment at the top
   defining a special codec, which could also

3. Addition of a standard import hook in the standard library which could
   be used, like the special encoding example above, to implement
   syntactic changes.

By doing searches in standard locations (Github, Gitlab, etc.) on, one could
identify how many modules are making use of a given experimental syntax,
giving an idea of the desirability of incorporating into Python.

Imagine how different the discussion about the walrus operator would have been
if people had had the opportunity to try it out on their own for a few months
prior to a decision being made about adding it to Python.

## New Syntax: two approaches

There are currently at least two ways in which one can write a Python program
that can use some non standard syntax:

* By using an import hook. This is the most powerful approach as it
  allows one to do changes either at the source level
  (prior to parsing), or at the AST level, or both.

* By using a custom encoding. This only allows transformations at the source level.

Both approaches currently require a two-step process.

To use an import hook, one has first to load a function that sets up this import hook before importing the module that contains the experimental syntax.  This makes it impossible to simply write

```
python module_with_new_syntax.py
```
and have it being executed.  Import hooks, like the name implies,
only apply to modules being imported - not to the first module executed by Python.

With a custom encoding, it is however possible to first register a
custom codec either via a site.py or usercustomize.py file.
Once this is done, the above way of running a module with new syntax is possible,
provided that the appropriate encoding declaration is included in the script.
This is what I did with the example shown above.


### Current limitation of these two approaches

Using an import hook for enabling new syntax does not work
for code entered in the standard Python REPL, which limits the possibility of experimentation.

While I have read that specifying the environment
variable `PYTHONIOENCODING` enables the Python REPL to use a custom encoding,
I have not been able to make it work on Windows and
confirm that it is indeed possible to do so.

However, I have been able to use a simple customized REPL that can make use
of the above.  Perhaps the standard REPL could be modified in a similar way.

## New suggested process

Assuming one of the options mentioned above is adopted,
before changes to the syntax are introduced in a Python version,
they would be made available to be used either as an encoding variant
or an import hook giving enough time for interested pythonistas to
experiment with the new syntax, writing actual code and possibly
trying out various alternatives.


## Proof of concept

As a proof of concept shown at the beginning of this post,
I have created two tiny modules that introduce new syntax that
had been discussed many times on this list:

1. a new syntax for decimal literals
2. a new syntax for rationals

Both modules have been uploaded separately to Pypi;
I wanted to simulate what could happen if a proposal such
as this one were adopted.

To make use of these, you need to use the `experimental-syntax` codec
found in my `ideas` package.

To run the example as shown above, you first need to register the codec,
which can be done by using either the `site.py` or `usercustomize.py`
approach.

I chose the latter, by setting the environment variable `PYTHONPATH`  to be
a path where the following `usercustomize.py` file is found.

```python

from ideas import experimental_syntax_encoding

print(f"  --> {__file__} was executed")
```

Doing this on Windows, I found that it did not seem to work when
using a virtual environment (I added the print statement to confirm
that it was loaded).

Here's a sample session using the code available currently on pypi.

```
C:\Users\andre\github\ideas>python simple_test.py
  --> C:\Users\andre\github\ideas\usercustomize.py was executed
simple_test.py ran successfully.

C:\Users\andre\github\ideas>python
  --> C:\Users\andre\github\ideas\usercustomize.py was executed
Python 3.8.4 (tags/v3.8.4:dfa645a, Jul 13 2020, 16:30:28) [MSC v.1926 32 bit (Intel)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> from ideas import experimental_syntax_encoding
>>> from ideas import console
>>> console.start()
Configuration values for the console:
    transform_source: <function transform_source at 0x00A8AE38>
--------------------------------------------------
Ideas Console version 0.0.19. [Python version: 3.8.4]

~>> import simple_test
simple_test.py ran successfully.
~>> from experimental-syntax import decimal_literal
~>> 3.46D
Decimal('3.46')
~>> from experimental-syntax import fraction_literal
~>> 2/3F
Fraction(2, 3)
~>>
```


Installation:

python -m pip install ideas  # will also install token-utils
python -m pip install decimal-literal
python -m pip install fraction-literal

More information about "ideas" can be found at
https://aroberge.github.io/ideas/docs/html/

