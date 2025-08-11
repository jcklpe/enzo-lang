#!/usr/bin/env python3
"""Debug nested loop end-loop issue"""

import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing
_env.clear()
_initialize_builtin_variants()

print("Testing nested loop end-loop...")
print("=" * 50)

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
