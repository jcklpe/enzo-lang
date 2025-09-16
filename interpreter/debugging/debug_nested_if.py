#!/usr/bin/env python3

import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing
_env.clear()
_initialize_builtin_variants()

print("=== TESTING NESTED IF REBINDING ===")

test_code = '''
$should_swap: False;
$order: "ascending";
'''

ast = parse(test_code)
result = eval_ast(ast)
print(f"After variable declaration: {_env.get('$should_swap')}")
print(f"_env contents: {dict(_env)}")

print("\n=== TESTING NESTED IF PATTERN ===")

nested_test_code = '''
If $order is "ascending", (
    If 64 is greater than 34, (
        $should_swap <: True;
    );
);
'''

try:
    ast = parse(nested_test_code)
    result = eval_ast(ast)
    print(f"After nested If rebinding: {_env.get('$should_swap')}")
    print(f"_env contents: {dict(_env)}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

# Test the final value
final_test = '''
$should_swap;
'''

ast = parse(final_test)
result = eval_ast(ast)
print(f"\nFinal result: {result}")
print(f"Expected: True (VariantGroup(True))")
print(f"Test {'PASSED' if str(result) == 'True' else 'FAILED'}")