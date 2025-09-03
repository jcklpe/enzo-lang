#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing but preserve built-ins
_env.clear()
_initialize_builtin_variants()

print("=== ANALYZE FUNCTION AST ===")
test_code = '''
find-first-even: (
    param $list: [];
    Loop for $item in $list, (
        If ($item % 2) is 0, (
            return($item);
        );
    );
    return(False);
);
'''

print("Test code:")
print(test_code)
print("Parsing...")
ast = parse(test_code)

# Find the function definition
for stmt in ast:
    if hasattr(stmt, 'name') and stmt.name == 'find-first-even':
        func_ast = stmt.value
        print(f"Function is_multiline: {func_ast.is_multiline}")
        print(f"Function params: {func_ast.params}")
        print(f"Function local_vars: {func_ast.local_vars}")
        print(f"Function body length: {len(func_ast.body)}")
        for i, body_stmt in enumerate(func_ast.body):
            print(f"Body statement {i}: {type(body_stmt).__name__} - {body_stmt}")
        break
