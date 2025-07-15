#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from enzo_parser.parser import parse
from enzo_parser.ast_nodes import *

# Test parsing of simple destructuring
src1 = "$name1, $age1, $favorite-color1: $person1[];"
print("Parsing:", src1)
try:
    ast1 = parse(src1)
    print("AST:", ast1)
    print("Type:", type(ast1))
    if hasattr(ast1, 'source_expr'):
        print("Source expr:", ast1.source_expr)
        print("Source expr type:", type(ast1.source_expr))
except Exception as e:
    print("Error:", e)

print("\n" + "="*50 + "\n")

# Test parsing of reverse destructuring
src2 = "$person3[] :> $name3, $age3, $favorite-color3;"
print("Parsing:", src2)
try:
    ast2 = parse(src2)
    print("AST:", ast2)
    print("Type:", type(ast2))
    if hasattr(ast2, 'source_expr'):
        print("Source expr:", ast2.source_expr)
        print("Source expr type:", type(ast2.source_expr))
except Exception as e:
    print("Error:", e)
