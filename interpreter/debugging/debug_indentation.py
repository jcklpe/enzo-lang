#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.enzo_parser.parser import Parser

def debug_indentation():
    test_code = """$list-pipe
then ($this contains 4) :> $contains-four;"""

    print("=== TEST CODE ===")
    print(repr(test_code))

    try:
        parser = Parser(test_code)
        result = parser.parse()
    except Exception as e:
        print(f"\n=== CAUGHT ERROR ===")
        print(f"Error message: {e}")
        if hasattr(e, 'code_line'):
            print(f"Error code_line repr:")
            print(repr(e.code_line))
            print(f"Error code_line:")
            print(e.code_line)

            # Check each character
            print(f"\nCharacter analysis:")
            for i, char in enumerate(e.code_line):
                if char == '\n':
                    print(f"  {i:2}: '\\n'")
                elif char == ' ':
                    print(f"  {i:2}: ' ' (space)")
                elif char == '\t':
                    print(f"  {i:2}: '\\t' (tab)")
                else:
                    print(f"  {i:2}: '{char}'")

if __name__ == "__main__":
    debug_indentation()
