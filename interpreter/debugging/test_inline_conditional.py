#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Test the inline conditional assignment
_env.clear()
_initialize_builtin_variants()

test_code = '''$inline-test: "outer";
$result-scope: If True, ( $inline-test: "inner"; $inline-test ), Else, ( "never" );
"Result of inline If: <$result-scope>"; // Prints "inner"
"After inline If: <$inline-test>"; // Global is unaffected by the shadow. Prints "outer"
'''

print("=== Testing inline conditional assignment ===")
try:
    ast = parse(test_code)
    result = eval_ast(ast)
    print(f"Final result: {result}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

# Also test what each variable contains
print(f"\n$result-scope: {eval_ast(parse('$result-scope;'))}")
print(f"$inline-test: {eval_ast(parse('$inline-test;'))}")
