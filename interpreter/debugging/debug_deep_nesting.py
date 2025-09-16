#!/usr/bin/env python3

import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing
_env.clear()
_initialize_builtin_variants()

test_code = '''
"=== TESTING DEEP NESTING REBINDING ===";

$target: "original";
$target;

// Test 3-level nesting
If True, (
    "Level 1";
    If True, (
        "Level 2";
        If True, (
            "Level 3 - rebinding target";
            $target <: "changed_3_levels";
        );
    );
);

$target;

// Test 5-level nesting
$target2: "original2";
$target2;

If True, (
    "Level 1";
    If True, (
        "Level 2";
        If True, (
            "Level 3";
            If True, (
                "Level 4";
                If True, (
                    "Level 5 - rebinding target2";
                    $target2 <: "changed_5_levels";
                );
            );
        );
    );
);

$target2;
'''

print("=== TESTING DEEP NESTING ===")
try:
    ast = parse(test_code)
    result = eval_ast(ast)
    print(f"\nFinal result: {result}")

    # Check the final values
    print(f"target final value: {_env.get('$target')}")
    print(f"target2 final value: {_env.get('$target2')}")

    success1 = str(_env.get('$target')) == "changed_3_levels"
    success2 = str(_env.get('$target2')) == "changed_5_levels"

    print(f"3-level test: {'PASSED' if success1 else 'FAILED'}")
    print(f"5-level test: {'PASSED' if success2 else 'FAILED'}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()