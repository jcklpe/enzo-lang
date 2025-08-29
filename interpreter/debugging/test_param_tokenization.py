#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.enzo_parser.parser import parse

print("\n=== Simple param parsing ===")
try:
    ast = parse("param $n: ;")
    print(f"AST: {ast}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

print("\n=== Function with param ===")
try:
    ast = parse("(param $n: ; $n * 2)")
    print(f"Function AST: {ast}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

print("\n=== List with function ===")
try:
    ast = parse("[(param $n: ; $n * 2)]")
    print(f"List AST: {ast}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
