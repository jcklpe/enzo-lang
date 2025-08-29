#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing but keep built-ins
_env.clear()
_initialize_builtin_variants()

# Test function atoms in lists
test = '''$anon_ref_ops: [
    @(param $n: ; $n * 2),
    @(param $n: ; $n * $n),
    "not-a-function"
];
$anon_ref_ops.1(10);
'''

print("=== Test: Function atoms in lists ===")
try:
    ast = parse(test)
    result = eval_ast(ast)
    print(f"Result: {result}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

# Test simpler case
print("\n=== Test: Simple function in list ===")
_env.clear()
_initialize_builtin_variants()

test2 = '''$simple_list: [@(param $x: ; $x + 1)];
$simple_list;
'''

try:
    ast2 = parse(test2)
    result2 = eval_ast(ast2)
    print(f"Result: {result2}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
