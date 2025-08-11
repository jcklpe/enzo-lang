#!/usr/bin/env python3
import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env
from src.enzo_parser.parser import parse_program

# Reset environment for clean testing
_env.clear()

# Test with detailed logging
test_code = '''
$list-delete-current: ["a", "b", "c", "d"];
$visited-current: [];
"Starting with list:";
$list-delete-current;
Loop for $item in $list-delete-current, (
  "Processing item:";
  $item;
  "Before adding to visited:";
  $visited-current;
  [<$visited-current>, $item] :> $visited-current;
  "After adding to visited:";
  $visited-current;
  "Current list:";
  $list-delete-current;
  If $item is "b", (
      "Deleting current item 'b'";
      [$list-delete-current.1, $list-delete-current.3, $list-delete-current.4] :> $list-delete-current;
      "List after deletion:";
      $list-delete-current;
  );
  "---";
);
"Final visited:";
$visited-current;
"Final list:";
$list-delete-current;
'''

print("=== Detailed trace of current item deletion ===")
try:
    ast = parse_program(test_code)
    result = eval_ast(ast, value_demand=True)
    print(f"✓ Test completed")
    print("All results:")
    for i, res in enumerate(result):
        print(f"  {i}: {res}")

except Exception as e:
    print(f"✖ Runtime error: {e}")
    import traceback
    traceback.print_exc()
