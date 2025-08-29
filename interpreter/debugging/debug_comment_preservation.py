#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.enzo_parser.parser import parse

# Test comment preservation at different levels
test_cases = [
    # Top level variable invocation
    "$z-local; // error: undefined variable",

    # Variable invocation inside conditional
    """If True, (
    $if-var; // error: undefined variable (was defined in a separate scope)
);""",

    # Simple top level for comparison
    "$simple;",

    # Simple with comment
    "$simple; // some comment"
]

for i, test_code in enumerate(test_cases):
    print(f"\n=== Test Case {i+1} ===")
    print(f"Source: {repr(test_code)}")

    try:
        ast = parse(test_code)
        print(f"AST: {ast}")

        if isinstance(ast, list):
            for j, node in enumerate(ast):
                if hasattr(node, 'code_line'):
                    print(f"  Node {j} code_line: {repr(node.code_line)}")
                if hasattr(node, 'then_block') and node.then_block:
                    for k, sub_node in enumerate(node.then_block):
                        if hasattr(sub_node, 'code_line'):
                            print(f"    Sub-node {k} code_line: {repr(sub_node.code_line)}")

    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
