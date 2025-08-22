#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.enzo_parser.parser import parse

# Test the specific failing cases from lazy-syntax
test_cases = [
    '@list-name-lazy2: [$test-var: 50, 60, 70];',  # Should error on $test-var:
    'param $x: 50;'  # Should error on $x in param
]

for i, test_code in enumerate(test_cases, 1):
    print(f"=== Test Case {i} ===")
    print(f"Code: {test_code}")
    try:
        ast = parse(test_code)
        print("❌ Should have failed but didn't!")
        print("AST:", ast)
    except Exception as e:
        print(f"✅ Error (as expected): {e}")
    print()
