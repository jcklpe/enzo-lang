#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing but preserve built-ins
_env.clear()
_initialize_builtin_variants()

print("=== ANALYZING METHOD REFERENCE AST ===")

test_code = '''
$pet: [
    $name: "Spot",
    speak: (
        return("Woof! My name is <$self.name>");
    )
];

$ref-speak: @pet.speak;
$ref-speak;
'''

try:
    print("Parsing test...")
    ast = parse(test_code)

    # Print the AST structure
    print(f"AST: {ast}")

    # Look specifically at the last statement (the reference assignment)
    if hasattr(ast, 'statements') and len(ast.statements) >= 2:
        method_ref_statement = ast.statements[1]  # $ref-speak: @pet.speak;
        print(f"Method ref statement: {method_ref_statement}")

        if hasattr(method_ref_statement, 'value'):
            ref_value = method_ref_statement.value
            print(f"Reference value: {ref_value}")
            print(f"Reference value type: {type(ref_value)}")

            if hasattr(ref_value, 'target'):
                target = ref_value.target
                print(f"Reference target: {target}")
                print(f"Reference target type: {type(target)}")

    print("\nExecuting...")
    result = eval_ast(ast)
    print(f"Final result: {result}")

except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
