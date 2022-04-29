"""
.. admonition:: Summary

    Introduces four different forms using a ``repeat`` keyword.
    It also demonstrates how to use a callback parameters.


repeat as a keyword
=======================

Let's begin with an example.

.. code-block::

    > python -m ideas -a repeat --show
    Ideas Console version 0.0.38. [Python version: 3.9.10]

    ideas> repeat 3:
       ...     print('Hello')
       ...
    ===========Transformed============
    for _9e4a6946f8d44ffca90dc9475537d39a in range( 3):
        print('Hello')

    -----------------------------
    Hello
    Hello
    Hello

    ideas>

As you can see, ``repeat n``, where ``n`` is an integer,
is converted into a for loop, with a randomly named
variable, guaranteed not to have a name used for another
object in the program.  This works well in practice.

However, suppose we wish to do some repeatable tests,
ensuring that the variable names are always the same
for all tests: we can do this using a 'callback parameter'.
This is a parameter that is given to the ``add_hook``
function used to create the import hook.
``add_hook`` must use Python dict to pass all required
callback parameters to ``create_hook``, so that they
can be passed back to the function used to transform the code.

Here's a second example using it.

.. code-block::

    >>> from ideas.examples import repeat
    >>> from ideas.console import start
    >>> from ideas.session import config
    >>> config.show_changes = True
    >>> repeat.add_hook(predictable_names=True)
    <IdeasMetaFinder object for ideas.examples.repeat>
    >>> start()
    Ideas Console version 0.0.38. [Python version: 3.9.10]

    ideas> repeat 3:
       ...     print('Hello')
       ...
    ===========Transformed============
    for _1 in range( 3):
        print('Hello')

    -----------------------------
    Hello
    Hello
    Hello

    ideas>

As you can see, the name of the for loop variable, ``_1``,
is much simpler ... and predictable.

You will need to have a look at the code for ``repeat.py`` to
fully understand how to use such callback parameters in your
own import hooks.


Adds ``repeat`` as a keyword to write loops. The four constructs supported
are::

    repeat n:
        # code

    repeat while condition:
        # code

    repeat until condition:
        # code

    repeat forever:
        # code

For example::

    repeat 3:
        a = 2
        repeat a*a:
            pass

is equivalent to::

    for unique_variable_name_1 in range(3):
        a = 2
        for unique_variable_name_2 in range(a*a):
            pass
"""
from ideas import import_hook, utils
import token_utils


class RepeatSyntaxError(Exception):
    """Currently, only raised when a repeat statement has a missing colon."""

    pass


def transform_source(source, callback_params=None, **_kwargs):
    """This function is called by the import hook loader and is used as a
    wrapper for the function where the real transformation is performed.

    It can use an optional parameter, ``callback_params``, which is
    a dict that can contain a key, ``"predictable_names"``, to indicate
    that variables created as loop counters should take a predictable form.
    """
    """Replaces instances of::

        repeat forever: -> while True:
        repeat while condition: -> while  condition:
        repeat until condition: -> while not condition:
        repeat n: -> for _uid in range(n):

    A complete repeat statement is restricted to be on a single line ending
    with a colon (optionally followed by a comment). If the colon is
    missing, a ``RepeatSyntaxError`` is raised.
    """
    if callback_params is None or "predictable_names" not in callback_params:
        predictable_names = False
    else:
        predictable_names = callback_params["predictable_names"]
    new_tokens = []
    if predictable_names:
        variable_name = utils.generate_predictable_names()
    else:
        variable_name = utils.generate_variable_names()

    for tokens in token_utils.get_lines(source):
        # a line of tokens can start with INDENT or DEDENT tokens ...
        first_token = token_utils.get_first(tokens)
        if first_token == "repeat":
            last_token = token_utils.get_last(tokens)
            if last_token != ":":
                raise RepeatSyntaxError(
                    "Missing colon for repeat statement on line "
                    + f"{first_token.start_row}\n    {first_token.line}."
                )

            repeat_index = token_utils.get_first_index(tokens)
            second_token = tokens[repeat_index + 1]
            if second_token == "forever":
                first_token.string = "while"
                second_token.string = "True"
            elif second_token == "while":
                first_token.string = "while"
                second_token.string = ""
            elif second_token == "until":
                first_token.string = "while"
                second_token.string = "not"
            else:
                first_token.string = "for %s in range(" % next(variable_name)
                last_token.string = "):"

        new_tokens.extend(tokens)

    return token_utils.untokenize(new_tokens)


def add_hook(predictable_names=False, **_kwargs):
    """Creates and adds the import hook in sys.meta_path.

    If ``predictable_names`` is set to ``True``, a callback parameter
    passed to the source transformation function will be used to
    create variable loops with predictable names."""
    callback_params = {"predictable_names": predictable_names}
    hook = import_hook.create_hook(
        transform_source=transform_source,
        callback_params=callback_params,
        hook_name=__name__,
    )
    return hook
