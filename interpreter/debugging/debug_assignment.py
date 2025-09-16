#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing but preserve built-ins
_env.clear()
_initialize_builtin_variants()

test_code = '''
simple-function: (
    param $input: [];
    $result: [999, 888, 777];
    return($result);
);

$test: [1, 2, 3];
"Before:";
$test;

// Test direct assignment
$direct-result: $simple-function($test);
"Direct result:";
$direct-result;

// Test :> assignment
$simple-function($test) :> $test;
"After :> assignment:";
$test;
'''

print("=== ASSIGNMENT OPERATOR TEST ===")
try:
    ast = parse(test_code)
    result = eval_ast(ast)
    print("Assignment test completed")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
