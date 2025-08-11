#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def parse_test_blocks(content):
    """Parse test content into blocks like the test runner does"""
    blocks = {}
    current_block = None
    current_lines = []

    lines = content.strip().split('\n')
    for line in lines:
        if line.startswith('//='):
            # Save previous block
            if current_block:
                blocks[current_block] = current_lines
            # Start new block
            current_block = line
            current_lines = []
        else:
            if current_block:
                current_lines.append(line)

    # Save last block
    if current_block:
        blocks[current_block] = current_lines

    return blocks

# Read the golden file
with open('tests/combined-tests.golden.enzo', 'r') as f:
    golden_content = f.read()

# Check if there's a recent output file
output_files = ['tests/combined-tests.enzo.output', 'combined-tests.enzo.output']
actual_content = None

for output_file in output_files:
    if os.path.exists(output_file):
        with open(output_file, 'r') as f:
            actual_content = f.read()
        break

if actual_content is None:
    print("No output file found. Run the test first.")
    sys.exit(1)

golden_blocks = parse_test_blocks(golden_content)
actual_blocks = parse_test_blocks(actual_content)

print("GOLDEN BLOCKS:")
for header in sorted(golden_blocks.keys()):
    print(f"  {header}")

print("\nACTUAL BLOCKS:")
for header in sorted(actual_blocks.keys()):
    print(f"  {header}")

print("\nMISMATCHES:")
# Check for blocks that exist in actual but not golden
for header in actual_blocks:
    if header not in golden_blocks:
        print(f"  EXTRA IN ACTUAL: {header}")

# Check for blocks that exist in golden but not actual
for header in golden_blocks:
    if header not in actual_blocks:
        print(f"  MISSING IN ACTUAL: {header}")

# Check the specific problematic block
problem_header = "//= COMPUTED INDEX: VARIABLE SHADOWING"
if problem_header in golden_blocks and problem_header in actual_blocks:
    print(f"\n{problem_header}:")
    print("GOLDEN:")
    for line in golden_blocks[problem_header]:
        print(f"  '{line}'")
    print("ACTUAL:")
    for line in actual_blocks[problem_header]:
        print(f"  '{line}'")
