#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing but preserve built-ins
_env.clear()
_initialize_builtin_variants()

print("=== TESTING EXACT SAME CODE AS TEST FILE ===")

# Copy the exact code from the test file
test_code = '''
//= METHOD REFERENCE WITH STATE MUTATION
$pet: [
    $name: "Spot",
    speak: (
        return("Woof! My name is <$self.name>");
    ),
    age-increment: (
        $self.age + 1 :> $self.age;
        return($self.age);
    ),
    $age: 5
];

$ref-age: @pet.age-increment;
$ref-age();                 // should increment $pet.age → 6
$ref-age();                 // should increment $pet.age → 7
$pet.age;                   // should print 7
'''

try:
    print("Executing exact test code...")
    ast = parse(test_code)
    result = eval_ast(ast)
    print(f"Final result: {result}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
