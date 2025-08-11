#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Read the current combined test file to see what it contains
with open('tests/combined-tests.enzo', 'r') as f:
    combined_content = f.read()

print("=== COMBINED TEST CONTENT (last 500 chars) ===")
print(combined_content[-500:])

print("\n=== LOOKING FOR LAST SECTIONS ===")
lines = combined_content.splitlines()
in_computed_section = False
computed_sections = []
current_section = None
current_lines = []

for line in lines:
    if line.startswith('//= COMPUTED INDEX:'):
        if current_section:
            computed_sections.append((current_section, current_lines[:]))
        current_section = line
        current_lines = []
        in_computed_section = True
    elif line.startswith('//=') and in_computed_section:
        # End of computed index sections
        if current_section:
            computed_sections.append((current_section, current_lines[:]))
        in_computed_section = False
        current_section = line
        current_lines = []
    elif current_section:
        current_lines.append(line)

# Add the last section
if current_section:
    computed_sections.append((current_section, current_lines[:]))

print("COMPUTED INDEX SECTIONS FOUND:")
for section, lines in computed_sections:
    if "COMPUTED INDEX:" in section:
        print(f"  {section}")
        for line in lines[:3]:  # First 3 lines
            print(f"    {repr(line)}")
        if len(lines) > 3:
            print(f"    ... ({len(lines)} total lines)")
