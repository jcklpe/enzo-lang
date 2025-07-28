#!/usr/bin/env python3

# Test reading the actual test file
from src.enzo_parser.parser import parse_program
from src.evaluator import eval_ast

test_file = "tests/test-modules/control-flow.enzo"

print("=== TESTING ACTUAL TEST FILE ===")
print(f"Reading: {test_file}")

try:
    with open(test_file, 'r') as f:
        content = f.read()

    print(f"File length: {len(content)} characters")
    print("First few lines:")
    for i, line in enumerate(content.split('\n')[:10]):
        print(f"  {i+1}: {repr(line)}")

    print("\nLooking for For loop section...")
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'SIMPLE FOR LOOP' in line:
            print(f"Found For loop section at line {i+1}")
            for j in range(max(0, i-2), min(len(lines), i+8)):
                marker = " >>> " if j == i else "     "
                print(f"{marker}{j+1}: {repr(lines[j])}")
            break

    print("\nParsing full file...")
    ast = parse_program(content)
    print("✅ Parsed successfully!")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
