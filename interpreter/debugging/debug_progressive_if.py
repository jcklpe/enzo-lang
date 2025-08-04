#!/usr/bin/env python3

import sys
sys.path.append("../src")

from src.enzo_parser.parser import Parser

# Test with the first few sections to find where it breaks
test_content = '''//= SIMPLE IF TEST
$status-if: "ready";

If $status-if, (
  "Ready!"; // should print "Ready!"
);

//= IF CONDITION NOT MET and not
$status-if-empty: "";

If $status-if-empty, (
  "Won't print"; // shouldn't print
);

If not $status-if-empty, (
  "this should print"; // should print
);'''

print("=== TESTING FIRST THREE IF STATEMENTS ===")
print(f"Content length: {len(test_content)}")

try:
    parser = Parser(test_content)
    result = parser.parse()
    print("Parse successful!")
    print(f"Number of statements: {len(result)}")
except Exception as e:
    print(f"Error: {e}")
    print(f"Error type: {type(e)}")
    if hasattr(e, 'code_line'):
        print(f"Error code_line: {repr(e.code_line)}")

    # Print parser state for debugging
    print(f"Parser position: {parser.pos}/{len(parser.tokens)}")
    if parser.pos < len(parser.tokens):
        print(f"Current token: {parser.tokens[parser.pos]}")
        print(f"Previous few tokens:")
        for i in range(max(0, parser.pos-3), min(len(parser.tokens), parser.pos+3)):
            marker = " --> " if i == parser.pos else "     "
            print(f"{marker}Token {i}: {parser.tokens[i]}")

    import traceback
    traceback.print_exc()
