#!/usr/bin/env python3

import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing but preserve built-ins
_env.clear()
_initialize_builtin_variants()

print("=== Testing Rebinding Propagation ===")

# Test simple If -> Function nesting
test_code = '''
$test_var: "original";
$test_var;

If True, (
    "Level1-If";
    ($x: 1;
        "Level2-Function";
        $test_var <: "changed_by_nested_function";
    );
);

$test_var;
'''

try:
    ast = parse(test_code)
    result = eval_ast(ast)
    print(f"Final test_var value: {_env.get('test_var', 'NOT_FOUND')}")
    print(f"Expected: 'changed_by_nested_function'")
    print(f"Match: {_env.get('test_var') == 'changed_by_nested_function'}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()