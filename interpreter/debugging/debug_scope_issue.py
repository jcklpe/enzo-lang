#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing but preserve built-ins
_env.clear()
_initialize_builtin_variants()

print("=== Testing Variable Scoping in Loops within Functions ===")

# Test the specific scoping issue - function with loop
test_code = '''
$test_loop: (
    $list: [1, 2, 3];
    $count: 0;
    Loop for $item in $list, (
        $count + 1 :> $count;
    );
    $count;
);

$test_loop();
'''

print("Test code:")
print(test_code)
print()

try:
    ast = parse(test_code)
    result = eval_ast(ast)
    print("Result:", result)
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

print("\n=== Testing Global Loop (for comparison) ===")

# Reset environment
_env.clear()
_initialize_builtin_variants()

global_loop_code = '''
$list: [1, 2, 3];
$count: 0;
Loop for $item in $list, (
    $count + 1 :> $count;
);
$count;
'''

print("Global loop code:")
print(global_loop_code)
print()

try:
    ast = parse(global_loop_code)
    result = eval_ast(ast)
    print("Result:", result)
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

print("\n=== Testing Simple Function Rebinding (control) ===")

# Reset environment
_env.clear()
_initialize_builtin_variants()

simple_function_code = '''
$test_simple: (
    $count: 0;
    $count + 5 :> $count;
    $count;
);

$test_simple();
'''

print("Simple function code:")
print(simple_function_code)
print()

try:
    ast = parse(simple_function_code)
    result = eval_ast(ast)
    print("Result:", result)
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()