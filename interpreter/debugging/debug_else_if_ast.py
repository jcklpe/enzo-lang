#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.enzo_parser.parser import parse

# Test how else-if chains are parsed
test_code = '''$level-scope: 1;
If $level-scope is 0, (
    $msg-scope: "Level 0";
), Else if $level-scope is 1, (
    $msg-scope: "Level 1";
    "In Else If: <$msg-scope>";
), Else, (
    $msg-scope: "Other Level";
);'''

try:
    ast = parse(test_code)
    print("AST structure:")
    for i, node in enumerate(ast):
        print(f"Node {i}: {type(node)}")
        if hasattr(node, 'condition'):
            print(f"  Condition: {node.condition}")
        if hasattr(node, 'then_block'):
            print(f"  Then block: {len(node.then_block) if node.then_block else 0} statements")
        if hasattr(node, 'else_block'):
            print(f"  Else block: {len(node.else_block) if node.else_block else 0} statements")
        if hasattr(node, 'else_if_chain'):
            print(f"  Else if chain: {getattr(node, 'else_if_chain', 'NOT FOUND')}")

        # Check all attributes
        attrs = [attr for attr in dir(node) if not attr.startswith('_') and 'else' in attr.lower()]
        print(f"  Else-related attributes: {attrs}")

except Exception as e:
    print("Error:", e)
    import traceback
    traceback.print_exc()
