#!/usr/bin/env python3

import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing but preserve built-ins
_env.clear()
_initialize_builtin_variants()

print("=== Testing Execution Order ===")

test_code = '''
$deep_test: "original";
If True, (
    "Level1-If";
    ($x: 1;
        "Level2-Function";
    );
);
'''

try:
    ast = parse(test_code)
    result = eval_ast(ast)
    print(f"Final result: {result}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()