#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing but preserve built-ins
_env.clear()
_initialize_builtin_variants()

test_code = '''
// Test simple swap with 2-element list
swap-two: (
    param $list: [];

    $elem1: $list.1;
    $elem2: $list.2;

    $new-list: [$elem2, $elem1];
    return($new-list);
);

$test: [64, 34];
$test;

$swapped: $swap-two($test);
$swapped;
'''

print("=== SIMPLE SWAP TEST ===")
try:
    ast = parse(test_code)
    result = eval_ast(ast)
    print("Test completed successfully")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
