#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.enzo_parser.parser import parse

# Test the exact failing case from the anon-function-refs test
print("=== Testing exact failing case ===")
test_code = '''$anon_ref_ops: [
    @(param $n: ; $n * 2), // Doubler
    @(param $n: ; $n * $n), // Squarer
    "not-a-function"
];'''

try:
    ast = parse(test_code)
    print(f"Success! AST: {ast}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

# Test just the list part
print("\n=== Testing just the list ===")
list_code = '''[
    @(param $n: ; $n * 2),
    @(param $n: ; $n * $n),
    "not-a-function"
]'''

try:
    ast = parse(list_code)
    print(f"Success! AST: {ast}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

# Test just one @(...) element
print("\n=== Testing single @(...) ===")
single_code = '@(param $n: ; $n * 2)'

try:
    ast = parse(single_code)
    print(f"Success! AST: {ast}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
