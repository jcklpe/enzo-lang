#!/usr/bin/env python3
"""Debug live iteration with print statements"""

import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing
_env.clear()
_initialize_builtin_variants()

print("Debugging live iteration with detailed output...")
print("=" * 50)

test_code = '''
$dynamic-list: [1, 2];
$iterations-dynamic: 0;
Loop for $item in $dynamic-list, (
    "Item: <$item>";
    $iterations-dynamic + 1 :> $iterations-dynamic;
    If $item is 2, (
        [<$dynamic-list>, 3] :> $dynamic-list;
    );
    If $iterations-dynamic is 3, ( end-loop; );
);
$dynamic-list;
'''

try:
    print("Test code:")
    print(test_code)
    print("\nExecuting...")

    # Parse and evaluate
    ast = parse(test_code)
    result = eval_ast(ast)

    print("Final result:", result)

    # Check what's in the environment
    print("\nEnvironment state:")
    print("$dynamic-list =", _env.get('$dynamic-list', 'NOT FOUND'))
    print("$iterations-dynamic =", _env.get('$iterations-dynamic', 'NOT FOUND'))

except Exception as e:
    print("✗ Error:", e)
    import traceback
    traceback.print_exc()
