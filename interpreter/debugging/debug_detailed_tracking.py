#!/usr/bin/env python3
"""Debug the index tracking in detail"""

import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing
_env.clear()
_initialize_builtin_variants()

print("Debugging index tracking...")
print("=" * 50)

# Let's trace through what happens step by step
test_code = '''
$list-delete-behind: ["a", "b", "c"];
$visited-behind: [];
Loop for $item in $list-delete-behind, (
  [<$visited-behind>, "Processing:", $item, "at list:", $list-delete-behind] :> $visited-behind;
  If $item is "b", (
      [<$visited-behind>, "About to delete 'a' from:", $list-delete-behind] :> $visited-behind;
      [$list-delete-behind.2, $list-delete-behind.3] :> $list-delete-behind;
      [<$visited-behind>, "After deletion:", $list-delete-behind] :> $visited-behind;
  );
  [<$visited-behind>, "Final step - adding:", $item] :> $visited-behind;
);
$visited-behind;
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

    print(f"\n$visited-behind:")
    for i, item in enumerate(visited):
        print(f"  {i}: {item}")

    print(f"\n$list-delete-behind: {final_list}")

except Exception as e:
    print("✗ Error:", e)
    import traceback
    traceback.print_exc()
