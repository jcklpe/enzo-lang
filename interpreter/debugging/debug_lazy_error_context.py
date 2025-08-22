#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.enzo_parser.parser import parse

# Test the different error cases
test_cases = [
    '$lazy-var: 0; // error: cannot use `$` in variable declaration context',
    '$lazy-var2 <: 50; // error: cannot use `$` in rebind context',
    '50 :> $lazy-var2; // error: cannot use `$` in rebind context',
    '$list-name-lazy1: [50, 60, 70]; // error: cannot use `$` in variable declaration context'
]

for i, test_code in enumerate(test_cases):
    print(f"=== Test Case {i+1} ===")
    print(f"Code: {test_code}")

    try:
        ast = parse(test_code)
        print("❌ Should have failed but didn't!")
        print("AST:", ast)
    except Exception as e:
        print(f"✅ Error (as expected): {e}")
        if hasattr(e, 'code_line'):
            print(f"Error code_line: {repr(e.code_line)}")
        else:
            print("No code_line attribute")
    print()
