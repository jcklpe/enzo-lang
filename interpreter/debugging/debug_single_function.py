#!/usr/bin/env python3

import sys
import os

# Add the interpreter directory to the path so we can import src modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.enzo_parser.parser import parse

code = "[(param $x: ; $x + 1;), (param $x: ; $x * 2;)]"
print(f"Parsing function atom: {code}")
try:
    ast = parse(code)
    print(f"Success! AST: {ast}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
