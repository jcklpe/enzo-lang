#!/usr/bin/env python3
import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env
from src.enzo_parser.parser import parse

# Reset environment for clean testing
_env.clear()

# Test the actual case from the test suite
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

print("=== Testing the exact deletion case from test suite ===")
try:
    ast = parse(test_code)
    result = eval_ast(ast)
    print(f"✓ Test completed successfully")
    print(f"Final result: {result}")
except Exception as e:
    print(f"✖ Runtime error: {e}")
    import traceback
    traceback.print_exc()
