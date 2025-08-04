#!/usr/bin/env python3

import sys
sys.path.append("../src")

from src.enzo_parser.parser import Parser

# Test just the first IF statement that's failing
test_content = '''//= SIMPLE IF TEST
$status-if: "ready";

If $status-if, (
  "Ready!"; // should print "Ready!"
);'''

print("=== TESTING SIMPLE IF STATEMENT ===")
print(f"Content:\n{test_content}")

try:
    parser = Parser(test_content)
    result = parser.parse()
    print("Parse successful!")
    print(f"Result: {result}")
except Exception as e:
    print(f"Error: {e}")
    print(f"Error type: {type(e)}")
    if hasattr(e, 'code_line'):
        print(f"Error code_line: {repr(e.code_line)}")

    # Print parser state for debugging
    print(f"Parser position: {parser.pos}/{len(parser.tokens)}")
    if parser.pos < len(parser.tokens):
        print(f"Current token: {parser.tokens[parser.pos]}")
    print(f"In pipeline function: {parser.in_pipeline_function}")
    print(f"Pipeline start pos: {parser.pipeline_start_pos}")

    import traceback
    traceback.print_exc()
