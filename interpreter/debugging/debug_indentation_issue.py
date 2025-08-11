#!/usr/bin/env python3

import sys
sys.path.append("../src")

from src.enzo_parser.parser import Parser

# Test content that should trigger the error
test_content = '''//= MULTI-STAGE PIPELINE WITH CONDITIONAL STEP ERROR
$list-pipe: [1,2,3,4];

$list-pipe
then ($this contains 4) :> $contains-four;  // error: comparison word in pipeline'''

print("Testing parser with multi-line content...")
print("Source content:")
for i, line in enumerate(test_content.split('\n')):
    print(f"Line {i}: '{line}' (length: {len(line)})")

print("\nTesting parser...")
try:
    parser = Parser(test_content)
    parser.parse()
except Exception as e:
    print(f"Error message: {e}")
    print(f"Error code_line: {repr(e.code_line)}")

    # Debug the lines in the error message
    if hasattr(e, 'code_line') and e.code_line:
        print("\nError message lines breakdown:")
        for i, line in enumerate(e.code_line.split('\n')):
            spaces = len(line) - len(line.lstrip())
            print(f"Line {i}: {spaces} leading spaces: {repr(line)}")

    # Let's also check where the pipeline statement starts in the source
    print(f"\nSource analysis:")
    start_idx = test_content.find('$list-pipe\nthen')
    if start_idx != -1:
        print(f"Pipeline statement starts at index {start_idx}")
        line_start = test_content.rfind('\n', 0, start_idx)
        if line_start == -1:
            actual_line_start = 0
        else:
            actual_line_start = line_start + 1
        print(f"Line start position would be: {actual_line_start}")

        # Extract the text from that position
        end_idx = test_content.find(';', start_idx) + 1
        extracted = test_content[actual_line_start:end_idx]
        print(f"Extracted text: {repr(extracted)}")

        # Show what happens with the line processing
        pipeline_lines = [f"  {line.strip()}" for line in extracted.split('\n') if line.strip()]
        formatted = '\n'.join(pipeline_lines)
        print(f"Formatted result: {repr(formatted)}")
