#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def examine_sections_around_computed_index():
    # Read the combined test file
    with open('tests/combined-tests.enzo', 'r') as f:
        test_content = f.read()

    # Read the combined golden file
    with open('tests/combined-tests.golden.enzo', 'r') as f:
        golden_content = f.read()

    # Find sections around computed index
    test_lines = test_content.splitlines()
    golden_lines = golden_content.splitlines()

    print("=== EXAMINING TEST FILE AROUND COMPUTED INDEX ===")
    in_computed = False
    for i, line in enumerate(test_lines):
        if "CONDITIONAL FLOW" in line or "COMPUTED INDEX" in line or in_computed:
            print(f"{i:3d}: {repr(line)}")
            in_computed = True
            if i > 0 and test_lines[i-1].startswith("//=") and not "COMPUTED INDEX" in test_lines[i-1]:
                break
        if in_computed and line.startswith("//=") and "COMPUTED INDEX" not in line:
            break

    print("\n=== EXAMINING GOLDEN FILE AROUND COMPUTED INDEX ===")
    in_computed = False
    for i, line in enumerate(golden_lines):
        if "CONDITIONAL FLOW" in line or "COMPUTED INDEX" in line or in_computed:
            print(f"{i:3d}: {repr(line)}")
            in_computed = True
            if i > 0 and golden_lines[i-1].startswith("//=") and not "COMPUTED INDEX" in golden_lines[i-1]:
                break
        if in_computed and line.startswith("//=") and "COMPUTED INDEX" not in line:
            break

    # Look specifically at the transition from conditional-flow to computed-index
    print("\n=== TRANSITION FROM CONDITIONAL-FLOW TO COMPUTED-INDEX ===")

    # Find conditional-flow end in test
    test_cond_end = -1
    for i, line in enumerate(test_lines):
        if "Conditional pipelining" in line:
            # Find the end of this section
            for j in range(i+1, len(test_lines)):
                if test_lines[j].startswith("//="):
                    test_cond_end = j-1
                    break

    # Find computed-index start in test
    test_comp_start = -1
    for i, line in enumerate(test_lines):
        if "COMPUTED INDEX: BASIC ADDITION" in line:
            test_comp_start = i
            break

    if test_cond_end >= 0 and test_comp_start >= 0:
        print("TEST FILE TRANSITION:")
        for i in range(max(0, test_cond_end-2), min(len(test_lines), test_comp_start+3)):
            print(f"{i:3d}: {repr(test_lines[i])}")

    # Do the same for golden file
    golden_cond_end = -1
    for i, line in enumerate(golden_lines):
        if "Conditional pipelining" in line:
            # Find the end of this section
            for j in range(i+1, len(golden_lines)):
                if golden_lines[j].startswith("//="):
                    golden_cond_end = j-1
                    break

    golden_comp_start = -1
    for i, line in enumerate(golden_lines):
        if "COMPUTED INDEX: BASIC ADDITION" in line:
            golden_comp_start = i
            break

    if golden_cond_end >= 0 and golden_comp_start >= 0:
        print("\nGOLDEN FILE TRANSITION:")
        for i in range(max(0, golden_cond_end-2), min(len(golden_lines), golden_comp_start+3)):
            print(f"{i:3d}: {repr(golden_lines[i])}")

if __name__ == "__main__":
    examine_sections_around_computed_index()
