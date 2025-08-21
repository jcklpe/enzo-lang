#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.enzo_parser.parser import Parser
from src.enzo_parser.parser import Parser

# Test the exact line from lazy-syntax.enzo
test_code = '''//= use of invocation in a storage context
$lazy-var: 0; // error: cannot use `$` in assignment context
@lazy-var2: 0;
$lazy-var2 <: 50; // error: cannot use `$` in rebind context
50 :> $lazy-var2; // error: cannot use `$` in rebind context'''

print("Original code:")
print(repr(test_code))
print("\nLines:")
lines = test_code.split('\n')
for i, line in enumerate(lines):
    print(f"{i+1}: {repr(line)}")

print("\nTokenizing and parsing to see error...")
try:
    parser = Parser(test_code)
    ast = parser.parse()
except Exception as e:
    print(f"Error: {e}")
    print(f"Error type: {type(e)}")
    if hasattr(e, 'code_line'):
        print(f"Error code_line: '{e.code_line}'")
    # Check if the error has a code_line attribute
    if hasattr(e, 'code_line'):
        print(f"Error code_line: {repr(e.code_line)}")
