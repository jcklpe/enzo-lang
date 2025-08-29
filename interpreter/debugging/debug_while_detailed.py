#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing but keep built-ins
_env.clear()
_initialize_builtin_variants()

# Test the exact sequence from the failing test
test_code = '''$active-while: True;
$counter-while: 0;
Loop while $active-while and $counter-while is less than 5, (
    $counter-while + 1 :> $counter-while;
    "Counter: <$counter-while>";

    If $counter-while is 5, (
        False :> $active-while;
        "Set active-while to False";
    );
);
"Final active-while: <$active-while>";
$active-while;
'''

print("=== Testing with detailed AST evaluation ===")
try:
    ast = parse(test_code)
    result = eval_ast(ast)
    print(f"Final result: {result}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

# Also test simpler rebinding in conditional
print("\n=== Testing simple rebinding in conditional ===")
_env.clear()
_initialize_builtin_variants()
simple_test = '''$test: True;
If True, (
    False :> $test;
    "Inside conditional: <$test>";
);
"Outside conditional: <$test>";
$test;
'''

try:
    ast = parse(simple_test)
    result = eval_ast(ast)
    print(f"Simple test result: {result}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
