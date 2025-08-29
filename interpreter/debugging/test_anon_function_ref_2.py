#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing but keep built-ins
_env.clear()
_initialize_builtin_variants()

# Test using @ reference to get the function object for comparison
test = '''$anon_ref: @(param $x: ; return($x + 1));
If @anon_ref is Function, (
    "It's a function!";
);
'''

print("=== Test: Using @anon_ref for type checking ===")
try:
    ast = parse(test)
    result = eval_ast(ast)
    print(f"Result: {result}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

# Test call after type check
print("\n=== Test: Function call after type check ===")
_env.clear()
_initialize_builtin_variants()

test2 = '''$anon_ref: @(param $x: ; return($x + 1));
@anon_ref;
$anon_ref(5);
'''

try:
    ast2 = parse(test2)
    result2 = eval_ast(ast2)
    print(f"Result: {result2}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
