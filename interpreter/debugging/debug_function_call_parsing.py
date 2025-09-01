#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment
_env.clear()
_initialize_builtin_variants()

print("=== TESTING PARSING OF FUNCTION CALLS ===")

# Test parsing of the problematic expression
test_expressions = [
    '$func($value)',
    '$my_func("text")',
    'anon_ref_apply( $my_func, "text" )',
]

for expr in test_expressions:
    print(f"\nParsing: {expr}")
    try:
        ast = parse(expr + ';')
        print(f"  AST: {ast}")
        print(f"  First statement type: {type(ast.statements[0])}")
        if hasattr(ast.statements[0], 'func'):
            print(f"  Function part: {ast.statements[0].func}")
            print(f"  Function type: {type(ast.statements[0].func)}")
    except Exception as e:
        print(f"  ERROR: {e}")

print("\n=== TESTING SPECIFIC ISSUE ===")
# Test the specific issue inside function definition
function_def = '''
test_func: (
    param $func: ();
    param $value: "";
    return( $func($value) );
);
'''

try:
    ast = parse(function_def)
    print("Function definition parsed successfully")
    print(f"AST: {ast}")
except Exception as e:
    print(f"ERROR parsing function: {e}")
