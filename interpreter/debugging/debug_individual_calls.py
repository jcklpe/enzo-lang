#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing but preserve built-ins
_env.clear()
_initialize_builtin_variants()

print("=== TESTING EACH FUNCTION CALL SEPARATELY ===")

print("\n--- First call: find-first-even([1, 3, 5, 8, 9]) ---")
test_code1 = '''
find-first-even: (
    param $list: [];
    "Debug: About to start loop";
    Loop for $item in $list, (
        "Debug: Processing item <$item>";
        If ($item % 2) is 0, (
            "Debug: Found even number, returning";
            return($item);
        );
    );
    "Debug: Loop finished, no even found";
    return(False);
);

find-first-even([1, 3, 5, 8, 9]);
'''

print("Executing first call...")
ast1 = parse(test_code1)
result1 = eval_ast(ast1)
print(f"Result1: {result1}")

print("\n--- Second call: find-first-even([1, 3, 5, 7, 9]) ---")
_env.clear()
_initialize_builtin_variants()

test_code2 = '''
find-first-even: (
    param $list: [];
    "Debug: About to start loop";
    Loop for $item in $list, (
        "Debug: Processing item <$item>";
        If ($item % 2) is 0, (
            "Debug: Found even number, returning";
            return($item);
        );
    );
    "Debug: Loop finished, no even found";
    return(False);
);

find-first-even([1, 3, 5, 7, 9]);
'''

print("Executing second call...")
ast2 = parse(test_code2)
result2 = eval_ast(ast2)
print(f"Result2: {result2}")
