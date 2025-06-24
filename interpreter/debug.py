#!/usr/bin/env python3
from lark import Lark, Transformer

grammar = """
?start: expr
?expr: atom
     | expr "+" atom   -> add
     | expr "*" atom   -> mul
?atom: NUMBER           -> number
     | "(" expr ")"     -> paren
%import common.NUMBER
%import common.WS
%ignore WS
"""

class AST(Transformer):
    def number(self, v): return int(v[0])
    def add(self, v): return ("add", v[0], v[1])
    def mul(self, v): return ("mul", v[0], v[1])
    def paren(self, v): return v[0]

parser = Lark(grammar, parser='lalr', transformer=AST())
tree = parser.parse("(10 + 5)")
print(tree)
