#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.enzo_parser.parser import parse

# Check what AST node () creates
test_code = 'param $func: ();'

print("=== CHECKING () AST NODE ===")
ast = parse(test_code)
print(f"AST: {ast}")
print(f"AST type: {type(ast)}")
if hasattr(ast[0], 'default_value'):
    print(f"Default value: {ast[0].default_value}")
    print(f"Default value type: {type(ast[0].default_value)}")
else:
    print("No default_value attribute found")
