Possibilities
=============

When a user-written Python module gets executed, here's an overview of
what normally happens behind the scene.  Let's call this module ``script``

1. A search is done on ``sys.path`` for Python file (extension .py or .pyw)
   matching the known extensions.
2. The information about the file is used to create a module that is
   essentially empty saved for a read-only dict containing information
   about the file name, location, etc.
3. The file is then is read as a series of bytes.
4. The content of the file is decoded to obtain the source as a string.
5. That source is converted into a series of tokens.
6. These tokens are transformed into a (concrete?) parse tree.
7. The result is further converted into an abstract syntax tree (AST).
8. The AST is converted into a control flow graph.
9. The control flow graph is used to obtain a bytecode representation.
10. That bytecode representation is executed in the module's dict.

``ideas`` can be used to make the following changes.

1a. Where the file can be located - it does not have to be in a location included in ``sys.path``.  (Example from Python cookbook)

1b. What file extension to look for. (many examples of my own)

2a. Give the possibility of using a different module creation method - need to find an example

2b. Use a different ``module.__class__`` (see example constants)

4a. Show an example with essentially a custom encoding

4b. Convert the source using ``re`` or ``tokenize`` (preferable)

5 and 6: impossible to replace individually

7a: can modify the AST

8: no access to this step

9a: can modify the bytecode representation

10a: can temporarily use a different dict than the read-only one defined for the module (see constants).

