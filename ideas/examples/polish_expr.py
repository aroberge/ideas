"""
.. admonition:: Summary

    - Demonstrates how to use an import hook to do custom parsing

Polish notation (parsing)
=========================


Expressions in Polish (prefix) notation are written with each
operator preceding its operands, allowing unambiguous expressions
with no need for parentheses or precedence rules.  For example:

    >>> + 3 8
    11
    >>> * 2 + 1 4
    10
    >>> * + 2 1 4
    12
    >>> +*+*+*+
    ... 1 2 3 4 5 6 7
    ... 8
    505

Each of these expressions is valid Polish notation, but none
of them is accepted by the Python parser.  Using an import
hook, we can provide our own parsing step to construct the
correct AST for the expression.  This module also implements
assignment in prefix form:

    >>> = x 8
    >>> x
    8
    >>> * x x
    64
"""
import ast
from ast import (
    Add,
    Assign,
    BinOp,
    Constant,
    Div,
    Expr,
    Interactive,
    Module,
    Mult,
    Name,
    Sub,
    fix_missing_locations,
    literal_eval,
)
import token
import token_utils
from typing import Iterable

from ideas import import_hook


class Parser:
    """
    Simple recursive descent parser for the following grammar::

        file:        a=stmt* ENDMARKER
        interactive: a=stmt ENDMARKER
        eval:        a=expr ENDMARKER

        stmt:
            | '=' a=NAME b=expr
            | expr

        expr:
            | NUMBER
            | NAME
            | ('+' | '-' | '*' | '/') expr expr
    """

    def __init__(self, tokens: Iterable[token_utils.Token], filename: str):
        self.tokengen = (t for t in tokens if t.type not in {token.NEWLINE, token.NL, token.COMMENT})
        self.lasttok, self.nexttok = None, next(self.tokengen)
        self.filename = filename

    def advance(self):
        tok = self.nexttok
        if self.nexttok.type != token.ENDMARKER:
            self.lasttok, self.nexttok = self.nexttok, next(self.tokengen)
        return tok

    def peekmatch(self, toktype, string=None):
        return self.nexttok.type == toktype and (string is None or self.nexttok.string == string)

    def match(self, toktype, string=None):
        if self.peekmatch(toktype, string):
            return self.advance()
        return None

    def expect(self, toktype, string=None):
        if not self.peekmatch(toktype, string):
            if string is not None:
                raise self._syntaxerror(f"expected {string!r}")
            else:
                raise self._syntaxerror(f"expected {token.tok_name[toktype]}")
        return self.advance()

    def _syntaxerror(self, msg, tok=None):
        if tok is None:
            tok = self.nexttok
        return SyntaxError(msg, (
            self.filename,
            tok.start_row,
            tok.start_col + 1,
            tok.line,
            tok.end_row,
            tok.end_col + 1,
        ))


    # Grammar rules

    def file(self) -> ast.Module:
        # file: stmt* ENDMARKER

        body = []
        while not self.peekmatch(token.ENDMARKER):
            body.append(self.stmt())
        self.expect(token.ENDMARKER)
        return Module(body=body, type_ignores=[])

    def interactive(self) -> ast.Interactive:
        # interactive: stmt ENDMARKER

        stmt = self.stmt()
        self.expect(token.ENDMARKER)
        return Interactive(body=[stmt])

    def eval(self) -> ast.expr:
        # eval: expr ENDMARKER

        expr = self.expr()
        self.expect(token.ENDMARKER)
        return expr

    def stmt(self, name=None) -> ast.stmt:
        # stmt:
        #     | '=' a=NAME b=expr
        #     | expr

        if self.match(token.OP, "="):
            name = self.expect(token.NAME)
            expr = self.expr()
            return Assign(
                targets=[Name(id=name.string, ctx=ast.Store())],
                value=expr
            )
        else:
            return Expr(value=self.expr())

    def expr(self) -> ast.expr:
        # expr:
        #     | NUMBER
        #     | NAME
        #     | ('+' | '-' | '*' | '/') expr expr

        OPS = {"+": Add, "-": Sub, "*": Mult, "/": Div}

        if (literal := self.match(token.NUMBER)):
            return Constant(value=literal_eval(literal.string))
        elif (name := self.match(token.NAME)):
            return Name(id=name.string, ctx=ast.Load())
        elif (op := self.match(token.OP)):
            if op.string not in OPS:
                raise self._syntaxerror(f"unrecognized operator {op.string!r}", op)
            first = self.expr()
            second = self.expr()
            return BinOp(
                left=first,
                op=OPS[op.string](),
                right=second
            )
        elif self.peekmatch(token.ENDMARKER):
            raise self._syntaxerror("unexpected EOF")
        else:
            raise self._syntaxerror("invalid syntax")


def parse_source(src, filename, mode, **_kwargs):
    """Parses the source code into an AST"""
    parser = Parser(token_utils.tokenize(src), filename)
    if mode == "single":
        try:
            tree = parser.interactive()
        except SyntaxError as e:
            # Allow interactive entry over multiple lines
            if e.msg == "unexpected EOF":
                return None
            raise
    elif mode == "exec":
        tree = parser.file()
    elif mode == "eval":
        tree = parser.expr()
    else:
        raise ValueError("unrecognized parsing mode")

    return fix_missing_locations(tree)


def add_hook(**_kwargs):
    """Creates and automatically adds the import hook in sys.meta_path"""
    hook = import_hook.create_hook(
        hook_name=__name__,
        parse_source=parse_source,
    )
    return hook
