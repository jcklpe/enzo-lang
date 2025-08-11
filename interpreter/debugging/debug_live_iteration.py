#!/usr/bin/env python3
"""Debug live iteration appending"""

import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing
_env.clear()
_initialize_builtin_variants()

print("Testing live iteration appending...")
print("=" * 50)

test_code = '''
$dynamic-list: [1, 2];
$iterations-dynamic: 0;
Loop for $item in $dynamic-list, (
    "Item: <$item>"; // should print 1, 2, 3
    $iterations-dynamic + 1 :> $iterations-dynamic;
    "Iteration count: <$iterations-dynamic>";
    "Current list: <$dynamic-list>";
    If $item is 2, (
        "Appending 3 to list...";
        [<$dynamic-list>, 3] :> $dynamic-list;
        "List after append: <$dynamic-list>";
    );
    If $iterations-dynamic is 3, (
        "Safety break triggered";
        end-loop;
    ); // safety break
);
"Final list: <$dynamic-list>";
'''

try:
    print("Parsing code:")
    print(test_code)
    ast = parse(test_code)
    print("✓ Parsing successful!")

    print("\nEvaluating...")
    result = eval_ast(ast)
    print("✓ Evaluation successful!")
    print("All results:", result)

except Exception as e:
    print("✗ Error:", e)
    import traceback
    traceback.print_exc()
