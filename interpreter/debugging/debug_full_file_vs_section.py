#!/usr/bin/env python3

import sys
sys.path.append("../src")

from src.enzo_parser.parser import Parser

# Read the EXACT content from the test file
test_file_path = "tests/test-modules/conditional-flow.enzo"
with open(test_file_path, 'r') as f:
    full_content = f.read()

print("=== FULL FILE TEST ===")
print(f"File length: {len(full_content)}")

# Find the exact section
section_start = full_content.find("//= MULTI-STAGE PIPELINE WITH CONDITIONAL STEP ERROR")
section_end = full_content.find("//= Has function and pipeline")

if section_start == -1 or section_end == -1:
    print("Could not find the test section")
    exit(1)

section_content = full_content[section_start:section_end].strip()
print(f"Section content:\n{repr(section_content)}")

print("\n=== TESTING WITH FULL FILE CONTENT ===")
try:
    parser = Parser(full_content)
    parser.parse()
except Exception as e:
    print(f"Error: {e}")
    print(f"Error code_line: {repr(e.code_line)}")

    # Analyze the error message line by line
    if hasattr(e, 'code_line') and e.code_line:
        print("\nError message analysis:")
        for i, line in enumerate(e.code_line.split('\n')):
            spaces = len(line) - len(line.lstrip())
            print(f"  Line {i}: {spaces} spaces: {repr(line)}")

print("\n=== TESTING WITH ISOLATED SECTION ===")
# Also test with just the isolated section
isolated_content = '''//= MULTI-STAGE PIPELINE WITH CONDITIONAL STEP ERROR
$list-pipe: [1,2,3,4];

$list-pipe
then ($this contains 4) :> $contains-four;  // error: comparison word in pipeline'''

try:
    parser = Parser(isolated_content)
    parser.parse()
except Exception as e:
    print(f"Error: {e}")
    print(f"Error code_line: {repr(e.code_line)}")

    # Analyze the error message line by line
    if hasattr(e, 'code_line') and e.code_line:
        print("\nError message analysis:")
        for i, line in enumerate(e.code_line.split('\n')):
            spaces = len(line) - len(line.lstrip())
            print(f"  Line {i}: {spaces} spaces: {repr(line)}")
