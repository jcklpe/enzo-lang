#!/usr/bin/env python3
"""Debug the exact end-loop issue"""

import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing
_env.clear()
_initialize_builtin_variants()

test_code = '''
$numbers: [1, 2, 3, 8, 9, 10];
$sum: 0;
Loop for $num in $numbers, (
    If $num is 8, (
        "Found 8, ending loop.";
        end-loop;
    );
    If ($num % 2) is not 0, (
        restart-loop;
    );
    $sum + $num :> $sum;
);
$sum;
'''

print("Testing end-loop issue...")
print("=" * 50)

try:
    ast = parse(test_code)
    result = eval_ast(ast)
    print(f"Final result: {result}")
    print(f"Sum: {_env.get('$sum')}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
