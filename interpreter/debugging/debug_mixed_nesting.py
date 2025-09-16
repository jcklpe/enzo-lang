#!/usr/bin/env python3

import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing
_env.clear()
_initialize_builtin_variants()

test_code = '''
"=== TESTING MIXED NESTING ISSUE ===";

$target: "original";
$target;

If True, (
    "Debug1";
    ($x: 1;
        "Debug2";
        $target <: "changed";
        "Debug3";
    );
    "Debug4";
);

$target;
'''

print("=== TESTING MIXED NESTING ISSUE ===")
try:
    ast = parse(test_code)
    result = eval_ast(ast)
    print(f"\nFinal result: {result}")
    print(f"target final value: {_env.get('$target')}")

    success = str(_env.get('$target')) == "changed"
    print(f"Test: {'PASSED' if success else 'FAILED'}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()