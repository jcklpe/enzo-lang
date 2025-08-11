#!/usr/bin/env python3
"""Debug simplified live iteration"""

import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing
_env.clear()
_initialize_builtin_variants()

print("Testing simplified live iteration...")
print("=" * 50)

# Test the exact failing case
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
    ast = parse(test_code)
    result = eval_ast(ast)
    print("Final result:", result)

    # Let's also evaluate each statement individually to see the outputs
    print("\nStep by step execution:")
    # ast is a list of statements, not a Program object
    statements = ast if isinstance(ast, list) else [ast]
    for i, stmt in enumerate(statements):
        print(f"Statement {i+1}: {type(stmt).__name__}")
        try:
            individual_result = eval_ast(stmt)
            if individual_result is not None:
                print(f"  Output: {individual_result}")
        except Exception as e:
            print(f"  Error: {e}")

except Exception as e:
    print("✗ Error:", e)
    import traceback
    traceback.print_exc()
