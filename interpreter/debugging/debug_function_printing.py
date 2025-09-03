#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing but preserve built-ins
_env.clear()
_initialize_builtin_variants()

# Simple test to understand the current behavior
test_code = """
simple_func: (
    param $x: ;
    $x;
    $x + 1;
);

simple_func(5);
"""

print("=== SIMPLE FUNCTION TEST ===")
print("Test code:")
print(test_code)
print("\nParsing...")
ast = parse(test_code)

print("Executing...")
try:
    result = eval_ast(ast)
    print(f"Final result: {result}")
except Exception as e:
    print(f"Error: {e}")

print("\n" + "="*50)

# Now test the recursion case
rec_test_code = """
$rec_n: 100;
rec_countdown: (
    param $rec_n: ;
    $rec_n;
    If $rec_n is greater than 0, (
        $rec_n - 1 :> $rec_n;
        rec_countdown($rec_n);
    );
);

rec_countdown(2);
"Global n is still: <$rec_n>";
"""

print("\n=== RECURSION TEST ===")
print("Test code:")
print(rec_test_code)

_env.clear()
_initialize_builtin_variants()

print("\nParsing...")
ast = parse(rec_test_code)

print("Executing...")
try:
    result = eval_ast(ast)
    print(f"Final result: {result}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

print(f"\nGlobal rec_n after execution: {_env.get('rec_n', 'NOT FOUND')}")
print(f"Global $rec_n after execution: {_env.get('$rec_n', 'NOT FOUND')}")
