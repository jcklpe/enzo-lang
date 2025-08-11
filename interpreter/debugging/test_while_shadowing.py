#!/usr/bin/env python3

import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env
from src.enzo_parser.parser import parse

# Reset environment for clean testing
_env.clear()

# Test the while loop shadowing case
test_code = """
$iteration52: 0;
$iteration52; // prints 0
Loop while $iteration52 is less than 3, (
    $local-var: 1;
    $local-var;  // prints 1 each loop
    $local-var + 1 :> $local-var;
    $local-var; // prints 2 each loop
    $iteration52 + 1 :> $iteration52;
    $iteration52; // prints 1, 2, 3
);

$iteration52; // prints 3
"""

try:
    ast = parse(test_code)
    result = eval_ast(ast)
    print(f"Test completed successfully!")
    print(f"Results: {result}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
