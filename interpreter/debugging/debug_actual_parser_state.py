#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.enzo_parser.parser import Parser

def debug_actual_parser():
    test_code = """$list-pipe
then ($this contains 4) :> $contains-four;"""

    print("=== TEST CODE ===")
    print(repr(test_code))

    try:
        parser = Parser(test_code)
        # Add some debugging to track what happens
        print(f"\n=== PARSER STATE ===")
        print(f"parser.pipeline_start_pos initial: {parser.pipeline_start_pos}")

        # Try to parse - this should trigger the error
        result = parser.parse()
    except Exception as e:
        print(f"\n=== CAUGHT ERROR ===")
        print(f"Error type: {type(e).__name__}")
        print(f"Error message: {e}")
        if hasattr(e, 'code_line'):
            print(f"Error code_line:")
            print(repr(e.code_line))

if __name__ == "__main__":
    debug_actual_parser()
