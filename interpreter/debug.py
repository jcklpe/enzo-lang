#!/usr/bin/env python3
from src.parser import parse
from lark import Tree

code = """
adder: (
param $x: 6;
param $y: 6;
return(($y + $x));
);

adder();
$adder();
"""

try:
    tree = parse(code)
    print("=== PARSED AST ===")
    print(tree)
except Exception as e:
    print("=== PARSE ERROR ===")
    print(e)
