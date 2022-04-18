.. admonition:: Summary

    Demonstrates how to use a callback parameters.


repeat as a keyword
=======================


We begin by two demonstrations, before going into more details
about the choices we made.


.. code-block::

    > python -m ideas -a repeat --show
    Ideas Console version 0.0.34. [Python version: 3.10.2]

    >>> repeat 3:
    ...    print('Hello')
    ...
    ===========Transformed============
    for _efedbc8c9e0b4d0194b0568321b8429e in range( 3):
       print('Hello')

    -----------------------------
    Hello
    Hello
    Hello
    >>>

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

Here's an example using it.

.. code-block::

    >>> from ideas.examples import repeat
    >>> from ideas.console import start
    >>> from ideas.session import config
    >>> config.show_changes = True
    >>> repeat.add_hook(predictable_names=True)
    <IdeasMetaFinder object for ideas.examples.repeat>
    >>> start()
    Ideas Console version 0.0.34. [Python version: 3.10.2]

    ~>> repeat 3:
    ...     print('Hello')
    ...
    ===========Transformed============
    for _1 in range( 3):
        print('Hello')

    -----------------------------
    Hello
    Hello
    Hello
    ~>>

As you can see, the name of the for loop variable, ``_1``,
is much simpler ... and predictable.

You will need to have a look at the code for ``repeat.py`` to
fully understand how to use such callback parameters in your 
own import hooks.

API for ``repeat``
--------------------

.. automodule:: ideas.examples.repeat
   :members:


.. note::

    The following text goes into some details about the origin
    of the ``repeat`` import hook. 
    It contains no additional information relevant for
    creating your own import hooks.


.. sidebar:: Learning from other experts

    The Quorum computing language has been designed based on evidence gathered
    from `how human learn programming languages <https://quorumlanguage.com/evidence.html>`_.

    It includes `three of the four repeat <https://quorumlanguage.com/tutorials/language/repeat.html>`_ choices mentioned above, with a slightly different syntax::

        repeat 10 times
            // code
        end

        repeat while condition
            // code
        end

        repeat until condition
            // code
        end

    In addition, Tobias Kohn, who created `TygerJython <http://jython.tobiaskohn.ch/>`_
    as part of his Ph.D. thesis, also found it useful to add such a keyword
    to Python as used in the TygerJython environment.


From blocks to textual code
---------------------------


Repeating a series of instructions is something that is often done when
running programs.  Block-based programming environments, such as
`Scratch <https://scratch.mit.edu/>`_,
`Blockly <https://developers.google.com/blockly/>`_,
`GP <https://gpblocks.org/>`_, etc,
have different blocks that can be used for this purpose.  For example:

.. image:: _static/repeat10.png
   :scale: 100 %
   :alt: Repeat 10 block

.. image:: _static/repeat_until.png
   :scale: 100 %
   :alt: Repeat until block

and a "repeat forever" loop (shown in French below):

.. image:: _static/repeat_forever_fr.png
   :scale: 55 %
   :alt: French repeat forever block


Depending on the block-based environment one uses, there are up to four
four main such cases, which can be written as follows
in standard Python::

    for _ in range(n):
        '''Repeat a series of instruction n times, without having to
           keep track of the specific iteration number
        '''

    while condition:
        '''Repeat a series of instruction an unspecified number of times,
           while a certain condition is met.
        '''

    while not condition:
        '''Repeat a series of instruction an unspecified number of times,
           until a certain condition is met.
        '''

    while True:
        '''Repeat a series of instruction an unspecified number of times,
           until a something inside the loop triggers a "break" to end the loop.
        '''

Inspired by the choices made by creators of block-based programming environments,
in my `AvantPy project <https://aroberge.github.io/avantpy/docs/html/>`_,
I included a few additional keywords to cover the 4 cases above
in a natural way::

    repeat n:
        # code

    repeat while condition:
        # code

    repeat until condition:
        # code

    repeat forever:
        # code

Some motivation
-------------------

.. admonition:: First, TygerJython's explanation

    **Why did you add a «repeat»-statement to the language?**

    One of the most difficult aspects for programming novices are
    variables and loops, especially when combined.
    With the ``repeat``-statement we provide the means to create a looping
    construct without the need for variables.
    This way, you can introduce one concept after the other and make it easier for the students to understand them.
    So far, our experience with «repeat» has been very encouraging.


**Suppose that I am teaching programming to beginners using Python's turtle module.**
So far, we've only written programs that use one instruction per line::

    from turtle import forward, left

    # Draw a square

    forward(100)
    left(90)

    forward(100)
    left(90)

    forward(100)
    left(90)

    forward(100)
    left(90)

I wish to use this to show to students how we can have computers **repeat**
a given set of instructions, instead of typing them multiple times.
Using Python, here's the natural way to do this::

    from turtle import forward, left

    # Draw a square

    for variable in range(4):
        forward(100)
        left(90)

In doing so, I need to introduce all at once many new concepts and additional terms:

   1. the concept of an indented code block preceded by a colon;

   2. two keywords, ``for`` and ``in``;

   3. the use of a *variable*, which is some quantity with a completely irrelevant name in this example, except that it cannot be a keyword;

   4. the introduction of a built-in function, ``range()``, which, unlike ``forward()`` or ``left()``, does not have a visual representation.

By contrast, using the ``repeat`` keyword, the above can be written as::

    from turtle import forward, left

    # Draw a square

    repeat 4:
        forward(100)
        left(90)

and we only need to introduce fewer new topics:

   1. the concept of an indented code block preceded by a colon;

   2. one new keyword: ``repeat``.


A final word about the motivation
----------------------------------

We've already mentioned the usage in blocks-based programming environment
of ``repeat``, or some similar alternative in other languages. ``repeat``
was also the clearer possibility for people unfamiliar with programming jargon
as found by Andreas Stefik and Susanna Siebert, and published
"An Empirical Investigation into Programming Language Syntax."
ACM Transactions on Computing Education, 13(4), Nov. 2013.

