#!/usr/bin/env python3

import sys
import os

# Add the interpreter directory to the path so we can import src modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.enzo_parser.parser import parse

code = "$simple: (param $x: ; $x);"
print(f"Parsing: {code}")
ast = parse(code)
print(f"AST: {ast}")
print(f"AST statements: {ast.statements}")
for stmt in ast.statements:
    print(f"Statement: {stmt}")
    if hasattr(stmt, 'value') and hasattr(stmt.value, 'params'):
        print(f"  Function params: {stmt.value.params}")
