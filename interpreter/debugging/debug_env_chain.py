#!/usr/bin/env python3

import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing but preserve built-ins
_env.clear()
_initialize_builtin_variants()

print("=== Tracing Environment Chain ===")

# First, let's test if simple If nesting works
test_simple_if = '''
$test_var: "original";
If True, (
    If True, (
        $test_var <: "changed_by_if";
    );
);
$test_var;
'''

print("\n--- Testing Simple If Nesting ---")
try:
    ast = parse(test_simple_if)
    result = eval_ast(ast)
    print(f"Result: {_env.get('test_var', 'NOT_FOUND')}")
except Exception as e:
    print(f"Error: {e}")

# Reset for next test
_env.clear()
_initialize_builtin_variants()

# Now test simple function nesting
test_simple_func = '''
$test_var: "original";
($x: 1;
    ($y: 2;
        $test_var <: "changed_by_func";
    );
);
$test_var;
'''

print("\n--- Testing Simple Function Nesting ---")
try:
    ast = parse(test_simple_func)
    result = eval_ast(ast)
    print(f"Result: {_env.get('test_var', 'NOT_FOUND')}")
except Exception as e:
    print(f"Error: {e}")

# Reset for mixed test
_env.clear()
_initialize_builtin_variants()

# Test If -> Function
test_if_func = '''
$test_var: "original";
If True, (
    ($x: 1;
        $test_var <: "changed_if_func";
    );
);
$test_var;
'''

print("\n--- Testing If->Function Nesting ---")
try:
    ast = parse(test_if_func)
    result = eval_ast(ast)
    print(f"Result: {_env.get('test_var', 'NOT_FOUND')}")
except Exception as e:
    print(f"Error: {e}")