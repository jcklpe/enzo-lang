#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment
_env.clear()
_initialize_builtin_variants()

print("=== DEBUGGING STATEFUL COUNTER ===")

test_code = """
clos_make_counter: (
    $count: 0;
    return( @(
        $count + 1 :> $count;
        return($count);
    ) );
);

$clos_counter_A: clos_make_counter();
$clos_counter_A();
$clos_counter_A();
"""

try:
    ast = parse(test_code)
    result = eval_ast(ast)
    print(f"Result: {result}")
except Exception as e:
    print(f"ERROR: {e}")
    print(f"Error type: {type(e).__name__}")

print(f"\nFinal environment state: {dict(_env)}")
