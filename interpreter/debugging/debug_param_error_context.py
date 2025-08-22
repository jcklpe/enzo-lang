#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.enzo_parser.parser import parse

# Test just the problematic function
test_code = '''@lazy-function1: (
    param $x: 50;  // error: cannot use `$` in variable declaration context
    return($x + 1);
)'''

print(f"Test code:\n{test_code}\n")

try:
    ast = parse(test_code)
    print("✅ Parsing successful!")
    print("AST:", ast)

except Exception as e:
    print(f"❌ Error: {e}")
    print(f"Error type: {type(e)}")
    if hasattr(e, 'code_line'):
        print(f"Error code_line: {repr(e.code_line)}")
    import traceback
    traceback.print_exc()
