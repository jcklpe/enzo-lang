#!/usr/bin/env python3

# Debug the new conditional syntax parsing

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.enzo_parser.parser import Parser

# Test the specific syntax from subset-conditional-flow.enzo
test_cases = [
    # The exact failing case
    '$status-if: "ready"; If $status-if, ("Ready!");',

    # Simpler variations to isolate the issue
    'If $x, ("yes");',
    'If true, ("yes");',

    # Old syntax for comparison
    'If $x, "yes"; end;',

    # Test just the comma parsing
    '$x: 5; $x, $x;',
]

print("=== DEBUGGING NEW CONDITIONAL SYNTAX ===")

for i, code in enumerate(test_cases, 1):
    print(f"\nTest {i}: {code}")
    try:
        parser = Parser(code)
        ast = parser.parse()
        print(f"✅ Parsed successfully")
        print(f"AST: {ast[0] if ast else 'Empty'}")

    except Exception as e:
        print(f"❌ Parse error: {e}")

        # Try to find where in the parser this fails
        try:
            import traceback
            traceback.print_exc()
        except:
            pass
