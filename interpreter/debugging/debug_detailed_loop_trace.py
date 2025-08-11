#!/usr/bin/env python3
import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env
from src.enzo_parser.parser import parse

# Reset environment for clean testing
_env.clear()

# Test with detailed tracking
test_code = '''
$list-delete-behind: ["a", "b", "c"];
$visited-behind: [];
"Starting loop with list:";
$list-delete-behind;
"Starting with visited:";
$visited-behind;

Loop for $item in $list-delete-behind, (
  "Processing item:";
  $item;
  If $item is "b", (
      "Item is b, deleting a from list";
      [$list-delete-behind.2, $list-delete-behind.3] :> $list-delete-behind;
      "List after deletion:";
      $list-delete-behind;
  );
  "Adding item to visited list";
  [<$visited-behind>, $item] :> $visited-behind;
  "Visited list is now:";
  $visited-behind;
);

"Loop completed. Final visited list:";
$visited-behind;
"Final list:";
$list-delete-behind;
'''

print("=== Detailed loop tracing ===")
try:
    ast = parse(test_code)
    result = eval_ast(ast)
    print(f"✓ Test completed")
    print(f"Results: {result}")
except Exception as e:
    print(f"✖ Runtime error: {e}")
    import traceback
    traceback.print_exc()
