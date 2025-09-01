#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment
_env.clear()
_initialize_builtin_variants()

print("=== CHECKING AST OF PROBLEMATIC FUNCTION ===")

# Test the specific function that's causing issues
function_def = '''
anon_ref_apply: (
    param $func: ();
    param $value: "";
    return( $func($value) );
);
'''

try:
    ast = parse(function_def)
    print("Function definition parsed successfully")

    # Extract the function body
    binding = ast[0]  # Should be a Binding
    function_atom = binding.value  # Should be a FunctionAtom
    return_statement = function_atom.body[0]  # Should be a ReturnNode
    invoke_expression = return_statement.value  # Should be an Invoke

    print(f"Binding: {binding}")
    print(f"Function atom: {function_atom}")
    print(f"Return statement: {return_statement}")
    print(f"Invoke expression: {invoke_expression}")
    print(f"Invoke expression type: {type(invoke_expression)}")

    if hasattr(invoke_expression, 'func'):
        print(f"Function part: {invoke_expression.func}")
        print(f"Function part type: {type(invoke_expression.func)}")
        print(f"Arguments: {invoke_expression.args}")

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
