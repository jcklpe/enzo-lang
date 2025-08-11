#!/usr/bin/env python3
import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env
from src.enzo_parser.parser import parse_program

# Reset environment for clean testing
_env.clear()

# Test the second failing case
test_code = '''
$list-delete-current: ["a", "b", "c", "d"];
$visited-current: [];
Loop for $item in $list-delete-current, (
    [<$visited-current>, $item] :> $visited-current;
    If $item is "b", (
        [$list-delete-current.1, $list-delete-current.3, $list-delete-current.4] :> $list-delete-current;
    );
);
$visited-current;
$list-delete-current;
'''

print("=== Testing deletion of current item ===")
try:
    ast = parse_program(test_code)
    result = eval_ast(ast, value_demand=True)
    print(f"✓ Test completed")
    print(f"Result type: {type(result)}")
    print(f"Final results: {result}")

    if isinstance(result, list) and len(result) >= 2:
        print(f"Visited: {result[-2]} (expected: ['a', 'b', 'd'])")
        print(f"Final list: {result[-1]} (expected: ['a', 'c', 'd'])")

        if result[-2] == ["a", "b", "d"]:
            print("✓ Visited list is correct!")
        else:
            print("✖ Visited list is wrong")

        if result[-1] == ["a", "c", "d"]:
            print("✓ Final list is correct!")
        else:
            print("✖ Final list is wrong")

except Exception as e:
    print(f"✖ Runtime error: {e}")
    import traceback
    traceback.print_exc()
