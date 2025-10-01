#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing but preserve built-ins
_env.clear()
_initialize_builtin_variants()

test_code = '''
//= USING RESTART-LOOP AND END-LOOP
$numbers-for: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];
$sum-for: 0;
Loop for $num in $numbers-for, (
    If $num is 8, (
        "Found 8, ending loop.";
        end-loop;
    );
    If ($num % 2) is not 0, (
        // skip odd numbers
        restart-loop;
    );
    $sum-for + $num :> $sum-for; // only adds even numbers
);
$sum-for; // should be 2 + 4 + 6 = 12
'''

print("=== LOOP CONTROL PRINT TEST ===")
try:
    ast = parse(test_code)
    result = eval_ast(ast)
    print(f"\nFinal result: {result}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
