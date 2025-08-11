#!/usr/bin/env python3
import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env
from src.enzo_parser.parser import parse_program

# Reset environment for clean testing
_env.clear()

# Test with detailed logging
test_code = '''
$list-delete-behind: ["a", "b", "c"];
$visited-behind: [];
"Starting loop with list:";
$list-delete-behind;
Loop for $item in $list-delete-behind, (
  "Processing item:";
  $item;
  "Current visited:";
  $visited-behind;
  "Current list:";
  $list-delete-behind;
  If $item is "b", (
      "Deleting 'a' from list";
      [$list-delete-behind.2, $list-delete-behind.3] :> $list-delete-behind;
      "List after deletion:";
      $list-delete-behind;
  );
  [<$visited-behind>, $item] :> $visited-behind;
  "Added to visited, now:";
  $visited-behind;
  "---";
);
"Final visited:";
$visited-behind;
"Final list:";
$list-delete-behind;
'''

print("=== Detailed trace of live iteration ===")
try:
    ast = parse_program(test_code)
    result = eval_ast(ast, value_demand=True)
    print(f"✓ Test completed")
    print("Results:")
    for i, res in enumerate(result):
        print(f"  {i}: {res}")

except Exception as e:
    print(f"✖ Runtime error: {e}")
    import traceback
    traceback.print_exc()
