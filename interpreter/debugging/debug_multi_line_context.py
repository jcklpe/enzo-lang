#!/usr/bin/env python3

import sys
import os

# Add the src directory to the path so we can import from it
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Test the problematic multi-line context construction
test_src = """$list-pipe: [1,2,3,4];

$list-pipe
then ($this contains 4) :> $contains-four;"""

print("=== SOURCE ===")
print(repr(test_src))
print("\n=== LINES ===")
lines = test_src.split('\n')
for i, line in enumerate(lines):
    print(f"{i}: {repr(line)} -> stripped: {repr(line.strip())}")

print("\n=== PIPELINE DETECTION ===")
pipeline_lines = []
found_pipeline = False
for line in lines:
    stripped = line.strip()
    print(f"Line: {repr(line)}")
    print(f"Stripped: {repr(stripped)}")
    print(f"stripped == '$list-pipe': {stripped == '$list-pipe'}")
    print(f"found_pipeline: {found_pipeline}")
    if stripped == '$list-pipe' or found_pipeline:
        found_pipeline = True
        result_line = f"  {stripped}"
        print(f"Adding: {repr(result_line)}")
        pipeline_lines.append(result_line)
        if 'contains' in stripped and ';' in stripped:
            print("Breaking on contains + semicolon")
            break
    print("---")

print("\n=== FINAL RESULT ===")
multi_line_context = '\n'.join(pipeline_lines)
print(repr(multi_line_context))
print("\nFormatted:")
print(multi_line_context)
