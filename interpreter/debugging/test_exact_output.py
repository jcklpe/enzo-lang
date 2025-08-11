#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.enzo_parser.parser import Parser

def test_exact_output():
    test_code = """$list-pipe: [1,2,3,4];

$list-pipe
then ($this contains 4) :> $contains-four;"""

    print("=== FULL TEST CODE ===")
    print(repr(test_code))

    try:
        parser = Parser(test_code)
        result = parser.parse()
        print("=== NO ERROR - UNEXPECTED ===")
    except Exception as e:
        print(f"\n=== ERROR OUTPUT ===")
        print(f"Message: {e}")
        print(f"Code line: {repr(e.code_line)}")

        # Write to a file to compare exactly
        with open("debug_output.txt", "w") as f:
            f.write(str(e))
            f.write("\n")
            f.write(e.code_line)

        print(f"\nWrote output to debug_output.txt")

if __name__ == "__main__":
    test_exact_output()
