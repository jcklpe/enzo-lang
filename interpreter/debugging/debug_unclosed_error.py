#!/usr/bin/env python3
import sys
sys.path.append('..')

from src.enzo_parser.tokenizer import Tokenizer
from src.error_messaging import format_parse_error

# Test the exact failing case
test_code = """/' This is an open comment that never closes. // error: unclosed block comment
$e: 8;"""

print("=== TESTING UNCLOSED BLOCK COMMENT ERROR ===")
print(f"Test code: {repr(test_code)}")
print(f"Test code content:\n{test_code}")

try:
    tokenizer = Tokenizer(test_code)
    tokens = tokenizer.tokenize()
    print("ERROR: Should have failed but didn't!")
except Exception as e:
    print(f"\nCaught exception: {type(e).__name__}: {e}")

    # Test how format_parse_error handles this
    formatted = format_parse_error(e, src=test_code)
    print(f"\nFormatted error:\n{formatted}")

    # Test how it handles single line
    single_line = "/' This is an open comment that never closes. // error: unclosed block comment"
    try:
        tokenizer2 = Tokenizer(single_line)
        tokens2 = tokenizer2.tokenize()
        print("ERROR: Single line should have failed but didn't!")
    except Exception as e2:
        print(f"\nSingle line exception: {type(e2).__name__}: {e2}")
        formatted2 = format_parse_error(e2, src=single_line)
        print(f"\nSingle line formatted error:\n{formatted2}")
