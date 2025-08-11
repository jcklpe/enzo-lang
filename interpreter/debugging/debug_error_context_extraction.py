#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.enzo_parser.parser import Parser

def debug_error_context():
    test_code = """$list-pipe
then ($this contains 4) :> $contains-four;"""

    print("=== TEST CODE ===")
    print(repr(test_code))
    print("\n=== SIMULATING ERROR CONTEXT EXTRACTION ===")

    # Simulate what happens in the parser
    pipeline_start_pos = 0  # This is what gets set in parse_pipeline
    end_pos = 53  # This is what gets found by searching for semicolon

    # Extract the complete pipeline statement from start to end
    pipeline_text = test_code[pipeline_start_pos:end_pos]
    print(f"Raw pipeline text: {repr(pipeline_text)}")

    # Split into lines and format with consistent indentation
    pipeline_lines = [f"  {line.strip()}" for line in pipeline_text.split('\n') if line.strip()]
    multi_line_context = '\n'.join(pipeline_lines)

    print(f"Formatted multi-line context:")
    print(multi_line_context)

    print(f"\n=== EXPECTED OUTPUT ===")
    expected = """  $list-pipe
  then ($this contains 4) :> $contains-four"""
    print(expected)

if __name__ == "__main__":
    debug_error_context()
