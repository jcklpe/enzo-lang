#!/usr/bin/env python3

# Debug parentheses grouping vs function atoms

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.enzo_parser.parser import Parser

# Test different parentheses contexts to see what AST nodes are created
test_cases = [
    "($u + $v)",           # Simple arithmetic in parens
    "(5 + 3)",             # Literal arithmetic in parens
    "($x: 1; $x + 2)",     # Multi-statement function atom
    "2 * ($a + $b)",       # Parens for precedence
    "($result: 10; $result)", # Function with binding and return
]

print("=== ANALYZING PARENTHESES AS GROUPING VS FUNCTION ATOMS ===")

for i, code in enumerate(test_cases, 1):
    print(f"\nTest {i}: {code}")
    try:
        parser = Parser(code)
        ast = parser.parse()

        # Look at the AST structure
        if ast and len(ast) > 0:
            node = ast[0]
            print(f"AST Node Type: {type(node).__name__}")
            print(f"AST Details: {node}")

            # Check if it's a FunctionAtom
            if hasattr(node, 'body') and hasattr(node, 'params'):
                print("✅ This is a FunctionAtom (anonymous function)")
                print(f"   Body: {node.body}")
                print(f"   Params: {node.params}")
            elif hasattr(node, 'statements'):
                print("✅ This is a FunctionAtom (anonymous function)")
                print(f"   Statements: {node.statements}")
            else:
                print("❌ This is NOT a FunctionAtom")
                # Check what attributes it has
                attrs = [attr for attr in dir(node) if not attr.startswith('_')]
                print(f"   Available attributes: {attrs}")

    except Exception as e:
        print(f"❌ Parse error: {e}")
