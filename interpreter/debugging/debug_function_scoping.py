#!/usr/bin/env python3

import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment
_env.clear()
_initialize_builtin_variants()

# Test simple function atom rebinding
test_code = '''
$test: "original";
$test;  // should print "original"

// Test simple function atom rebinding
($dummy: 1;
    $test <: "changed_by_function";
);

$test;  // should print "changed_by_function"
'''

print("=== Testing Function Atom Rebinding ===")
ast = parse(test_code)
result = eval_ast(ast)
print(f"Final result: {result}")