#!/usr/bin/env python3
"""Debug live iteration with list deletion"""

import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing
_env.clear()
_initialize_builtin_variants()

print("Testing live iteration with list deletion...")
print("=" * 50)

test_code = '''
$list-delete-behind: ["a", "b", "c"];
$visited-behind: [];
Loop for $item in $list-delete-behind, (
  "Processing: <$item>";
  "List before: <$list-delete-behind>";
  If $item is "b", (
      "Deleting item 'a'";
      [$list-delete-behind.2, $list-delete-behind.3] :> $list-delete-behind;
      "List after deletion: <$list-delete-behind>";
  );
  [<$visited-behind>, $item] :> $visited-behind;
  "Visited so far: <$visited-behind>";
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

except Exception as e:
    print("✗ Error:", e)
    import traceback
    traceback.print_exc()
