#!/usr/bin/env python3
"""Debug nested for-loop restart-loop issue"""

import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing
_env.clear()
_initialize_builtin_variants()

print("Testing nested for-loop restart-loop...")
print("=" * 50)

test_code = '''
$matrix: [[1, 2], [3, 4]];
Loop for $row in $matrix, (
    "Processing row: <$row>";
    Loop for $cell in $row, (
        If $cell is 3, (
            "Found 3, restarting inner loop";
            restart-loop;
        );
        "Cell: <$cell>";
    );
);
'''

try:
    print("Test code:")
    print(test_code)
    print("\nExecuting...")

    ast = parse(test_code)
    result = eval_ast(ast)

    print("Result:", result)

except Exception as e:
    print("✗ Error:", e)
    import traceback
    traceback.print_exc()
