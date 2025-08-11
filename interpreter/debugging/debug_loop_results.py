#!/usr/bin/env python3
import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env
from src.enzo_parser.parser import parse

# Reset environment for clean testing
_env.clear()

# Test the exact failing case - but isolate each part
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
'''

print("=== Testing visited list result ===")
try:
    ast = parse(test_code)
    result = eval_ast(ast)
    print(f"✓ Test completed")
    print(f"Visited list result: {result}")

except Exception as e:
    print(f"✖ Runtime error: {e}")
    import traceback
    traceback.print_exc()

# Test just the final list
_env.clear()
test_code2 = '''
$list-delete-behind: ["a", "b", "c"];
$visited-behind: [];
Loop for $item in $list-delete-behind, (
  If $item is "b", (
      [$list-delete-behind.2, $list-delete-behind.3] :> $list-delete-behind;
  );
  [<$visited-behind>, $item] :> $visited-behind;
);
$list-delete-behind;
'''

print("\n=== Testing final list result ===")
try:
    ast = parse(test_code2)
    result = eval_ast(ast)
    print(f"✓ Test completed")
    print(f"Final list result: {result}")

except Exception as e:
    print(f"✖ Runtime error: {e}")
    import traceback
    traceback.print_exc()
