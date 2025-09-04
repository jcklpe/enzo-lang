#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing but preserve built-ins
_env.clear()
_initialize_builtin_variants()

print("=== LOOP INSIDE FUNCTION TEST ===")
test_code = '''
find-first-even: (
    param $list: [];
    "Starting loop for list: <$list>";
    Loop for $item in $list, (
        If ($item % 2) is 0, (
            return($item);
        );
    );
    "Loop finished, returning False";
    return(False);
);

find-first-even([1, 3, 5, 8, 9]);
find-first-even([1, 3, 5, 7, 9]);
'''

print("Test code:")
print(test_code)
print("Executing...")
ast = parse(test_code)
result = eval_ast(ast)
print(f"Final result: {result}")
