#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing but keep built-ins
_env.clear()
_initialize_builtin_variants()

# Test basic @(...) syntax
test1 = '''$anon_ref: @(param $x: ; return($x + 1));
$anon_ref(5);
'''

print("=== Test 1: Basic @(...) syntax ===")
try:
    ast1 = parse(test1)
    result1 = eval_ast(ast1)
    print(f"Result: {result1}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

# Test comparison with regular function atom
print("\n=== Test 2: Comparison with regular (...) ===")
_env.clear()
_initialize_builtin_variants()

test2 = '''$regular_ref: (param $x: ; return($x + 1));
$regular_ref(5);
'''

try:
    ast2 = parse(test2)
    result2 = eval_ast(ast2)
    print(f"Result: {result2}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

# Test type checking
print("\n=== Test 3: Type checking ===")
_env.clear()
_initialize_builtin_variants()

test3 = '''$anon_ref: @(param $x: ; return($x + 1));
If $anon_ref is Function, (
    "It's a function!";
);
'''

try:
    ast3 = parse(test3)
    result3 = eval_ast(ast3)
    print(f"Result: {result3}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
