#!/usr/bin/env python3
import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env
from src.enzo_parser.parser import parse_program

# Reset environment for clean testing
_env.clear()

# Test the exact failing case from the test suite
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

print("=== Testing live iteration with deletion behind iterator ===")
try:
    ast = parse_program(test_code)
    result = eval_ast(ast, value_demand=True)
    print(f"✓ Test completed")
    print(f"Result type: {type(result)}")
    print(f"Final results: {result}")

    # Expected results should be:
    # visited-behind: ["a", "b", "c"]
    # list-delete-behind: ["b", "c"]
    if isinstance(result, list) and len(result) >= 2:
        print(f"✓ Visited list: {result[-2]}")
        print(f"✓ Final list: {result[-1]}")
    else:
        print("✖ Unexpected result structure")

except Exception as e:
    print(f"✖ Runtime error: {e}")
    import traceback
    traceback.print_exc()
