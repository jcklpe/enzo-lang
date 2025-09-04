#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.enzo_parser.parser import parse
from src.evaluator import eval_ast, _env, _initialize_builtin_variants

print("=== TESTING BLOCK COMMENT PARSING AND EVALUATION ===")

# Reset environment
_env.clear()
_initialize_builtin_variants()

# Test the exact failing case
test_code = '''//= BLOCK COMMENT: COMMENTING OUT CODE
$z: 3;
/'
  // The following line should be ignored:
  $z <: 99;
'/
$z; // Should still be 3'''

print("Test code:")
print(test_code)
print()

try:
    print("Parsing...")
    ast = parse(test_code)
    print("AST created successfully")

    print("Evaluating...")
    result = eval_ast(ast)
    print(f"Result: {result}")

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
