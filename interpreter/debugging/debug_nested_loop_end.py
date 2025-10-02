#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing but preserve built-ins
_env.clear()
_initialize_builtin_variants()

test_code = '''
Loop, (
    "Outer loop started";
    $inner-count: 0;
    Loop, (
        "Inner loop running";
        $inner-count + 1 :> $inner-count;
        If $inner-count is 1, (
                "ending inner loop";
                end-loop;
        );
    );
    "Inner loop finished";
    end-loop;
    "shouldn't print";
);
'''

print("=== NESTED LOOP END DEBUG ===")
try:
    ast = parse(test_code)
    result = eval_ast(ast)
    print(f"\nFinal result: {result}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
