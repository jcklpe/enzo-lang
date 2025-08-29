#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.enzo_parser.parser import parse
from src.enzo_parser.ast_nodes import *

# Test how code_line is set during parsing
test_code = """$z-local; // error: undefined variable"""

try:
    ast = parse(test_code)
    print("AST:", ast)

    if isinstance(ast, list) and len(ast) > 0:
        node = ast[0]
        print(f"Node type: {type(node)}")
        print(f"Node code_line: {repr(getattr(node, 'code_line', 'NOT SET'))}")

        if hasattr(node, 'name'):
            print(f"Node name: {node.name}")

except Exception as e:
    print("Error:", e)
    import traceback
    traceback.print_exc()
