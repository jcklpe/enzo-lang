#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing but keep built-ins
_env.clear()
_initialize_builtin_variants()

# Test the comparison directly
test = '''$anon_ref: @(param $x: ; return($x + 1));
$anon_ref is Function;
'''

print("=== Testing direct comparison ===")
try:
    ast = parse(test)
    result = eval_ast(ast)
    print(f"Result: {result}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

# Test what type the function actually has
print("\n=== Testing actual type ===")
_env.clear()
_initialize_builtin_variants()

test2 = '''$anon_ref: @(param $x: ; return($x + 1));
@anon_ref;
'''

try:
    ast2 = parse(test2)
    result2 = eval_ast(ast2)
    print(f"Function object: {result2}")
    print(f"Type: {type(result2)}")
    print(f"Is EnzoFunction: {isinstance(result2, eval_ast(parse(''), env={}).get('EnzoFunction', type(None)))}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
