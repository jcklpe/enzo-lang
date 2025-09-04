#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing but preserve built-ins
_env.clear()
_initialize_builtin_variants()

print("=== TESTING METHOD REFERENCE IMPLEMENTATION ===")

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
    print("Testing method reference creation and invocation...")
    ast = parse(test_code)
    result = eval_ast(ast)
    print(f"Result: {result}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
