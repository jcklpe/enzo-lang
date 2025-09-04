#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing but preserve built-ins
_env.clear()
_initialize_builtin_variants()

print("=== DEBUGGING METHOD REFERENCE STATE MUTATION ===")

test_code = '''
$pet: [
    $name: "Spot",
    age-increment: (
        $self.age + 1 :> $self.age;
        return($self.age);
    ),
    $age: 5
];

$ref-age: @pet.age-increment;
$ref-age();
$ref-age();
$pet.age;
'''

try:
    print("Testing method reference with state mutation...")
    ast = parse(test_code)
    result = eval_ast(ast)
    print(f"Final result: {result}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
