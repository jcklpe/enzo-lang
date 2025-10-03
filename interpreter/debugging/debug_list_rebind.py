#!/usr/bin/env python3
"""Test list rebinding in loops."""

import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing but preserve built-ins
_env.clear()
_initialize_builtin_variants()

test_code = '''
test-func: (
    param $input: [1, 2, 3];

    $current: $input;
    $i: 1;

    Loop while $i is at most 2, (
        [99, $i] :> $current;
        $i + 1 :> $i;
    );

    return($current);
);

$result: test-func([5, 6, 7]);
$result;
'''

print("=== Testing list rebind in loop inside function ===")
ast = parse(test_code)
result = eval_ast(ast)
print(f"Result: {result}")