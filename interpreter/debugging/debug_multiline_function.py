#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing but preserve built-ins
_env.clear()
_initialize_builtin_variants()

test_code = '''
test_func: (
    5;
    "here is a text being printed";
    $x: "This is a piece of text saved to the $x keyname";
    $x;
    $x;
);

test_func();
'''

print("=== MULTILINE FUNCTION WITH NO RETURN ===")
print("Test code:")
print(test_code)
print("Executing...")
ast = parse(test_code)
result = eval_ast(ast)
print(f"Final result: {result}")
print(f"Final result type: {type(result)}")
