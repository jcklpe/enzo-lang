#!/usr/bin/env python3
"""Test the live deletion fix"""

import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing
_env.clear()
_initialize_builtin_variants()

print("Testing live deletion fix...")
print("=" * 50)

test_code = '''
$list-delete-behind: ["a", "b", "c"];
$visited-behind: [];
Loop for $item in $list-delete-behind, (
  If $item is "b", (
      [$list-delete-behind.2, $list-delete-behind.3] :> $list-delete-behind;
  );
  [<$visited-behind>, $item] :> $visited-behind;
);
$visited-behind;
$list-delete-behind;
'''

try:
    print("Test code:")
    print(test_code)
    print("\nExecuting...")

    ast = parse(test_code)
    result = eval_ast(ast)

    print("Final result:", result)

    # Check individual results
    visited = _env.get('$visited-behind', 'NOT FOUND')
    final_list = _env.get('$list-delete-behind', 'NOT FOUND')

    print(f"\n$visited-behind: {visited}")
    print(f"$list-delete-behind: {final_list}")

    # Expected results
    expected_visited = ["a", "b", "c"]
    expected_final = ["b", "c"]

    print(f"\nExpected visited: {expected_visited}")
    print(f"Expected final: {expected_final}")

    print(f"Visited matches: {visited == expected_visited}")
    print(f"Final matches: {final_list == expected_final}")

except Exception as e:
    print("✗ Error:", e)
    import traceback
    traceback.print_exc()
