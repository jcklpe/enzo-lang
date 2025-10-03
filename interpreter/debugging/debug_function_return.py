#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing but preserve built-ins
_env.clear()
_initialize_builtin_variants()

test_code = '''
// Test if we can even modify a list and return it from a function
modify-list: (
    param $input: [];

    "Input received:";
    $input;

    // Try to create a new list with different content
    $new-list: [999, 888];
    "New list created:";
    $new-list;

    return($new-list);
);

$original: [1, 2, 3];
"Original:";
$original;

$result: $modify-list($original);
"Result returned:";
$result;

"Original after function:";
$original;
'''

print("=== BASIC FUNCTION RETURN TEST ===")
try:
    ast = parse(test_code)
    result = eval_ast(ast)
    print("Test completed")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
