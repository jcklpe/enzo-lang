#!/usr/bin/env python3

# Debug script to check exactly what's being extracted from the real test file

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Read the actual test file
with open('tests/test-modules/conditional-flow.enzo', 'r') as f:
    content = f.read()

# Find the specific pipeline that's failing
lines = content.split('\n')
for i, line in enumerate(lines):
    if '$list-pipe' in line and 'then' not in line:
        print(f"Line {i+1}: {repr(line)}")
        # Look at the next few lines
        for j in range(1, 4):
            if i+j < len(lines):
                print(f"Line {i+j+1}: {repr(lines[i+j])}")
        break

print("\nLooking for the pipeline section...")
pipeline_start = None
for i, line in enumerate(lines):
    if line.strip() == '$list-pipe' and i+1 < len(lines) and 'then' in lines[i+1]:
        pipeline_start = i
        print(f"Found pipeline starting at line {i+1}")
        for j in range(5):  # Show next 5 lines
            if i+j < len(lines):
                print(f"  Line {i+j+1}: {repr(lines[i+j])}")
        break

# Now let's extract exactly what the parser would see
if pipeline_start is not None:
    # Get the line with $list-pipe
    first_line = lines[pipeline_start]
    second_line = lines[pipeline_start + 1]

    print(f"\nFirst line: {repr(first_line)}")
    print(f"Second line: {repr(second_line)}")

    # Reconstruct the pipeline text
    pipeline_text = first_line + '\n' + second_line.split('//')[0].rstrip()
    print(f"Combined pipeline text: {repr(pipeline_text)}")

    # Apply the current formatting logic
    pipeline_lines = [f"  {line.strip()}" for line in pipeline_text.split('\n') if line.strip()]
    formatted = '\n'.join(pipeline_lines)
    print(f"Formatted result: {repr(formatted)}")
    print("Formatted display:")
    print(formatted)
