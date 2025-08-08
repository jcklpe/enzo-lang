#!/usr/bin/env python3
"""Debug rebinding in while loop"""

import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing
_env.clear()
_initialize_builtin_variants()

test_code = '''
$active: True;
$active;
Loop while $active, (
    "In loop, active is:";
    $active;
    False :> $active;
    "After rebind, active is:";
    $active;
);
"After loop, active is:";
$active;
'''

print("Testing rebinding in while loop...")
print("=" * 50)

try:
    ast = parse(test_code)
    print("Parsed successfully")

    print("\nEvaluating:")
    result = eval_ast(ast)
    print(f"Final result: {result}")

    print(f"\nEnvironment state:")
    print(f"$active = {_env.get('$active', 'UNDEFINED')}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
