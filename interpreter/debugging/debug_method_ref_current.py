#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing but preserve built-ins
_env.clear()
_initialize_builtin_variants()

print("=== TESTING CURRENT METHOD REFERENCE CAPABILITY ===")

test_code = '''
$pet: [
    $name: "Spot",
    speak: (
        return("Woof! My name is <$self.name>");
    )
];

// Test 1: Basic property access (should work)
$pet.name;

// Test 2: Basic method call (should work)
$pet.speak();

// Test 3: Method reference (this is what we need to implement)
$ref-speak: @pet.speak;
'''

try:
    print("Parsing and executing test...")
    ast = parse(test_code)
    result = eval_ast(ast)
    print(f"Final result: {result}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
