#!/usr/bin/env python3

import sys
sys.path.append("../src")

from src.enzo_parser.parser import Parser
from src.enzo_parser.tokenizer import Tokenizer

# Read the full test file but focus on the problematic section
test_file_path = "tests/test-modules/conditional-flow.enzo"
with open(test_file_path, 'r') as f:
    full_content = f.read()

# Find just the problematic section in the full file
section_start = full_content.find("$list-pipe\nthen ($this contains 4)")
if section_start == -1:
    print("Could not find the pipeline section")
    exit(1)

section_end = full_content.find(";", section_start) + 1
pipeline_section = full_content[section_start:section_end]

print("=== PIPELINE SECTION IN FULL FILE ===")
print(f"Section starts at position: {section_start}")
print(f"Section content: {repr(pipeline_section)}")

# Find line start for this section
line_start = full_content.rfind('\n', 0, section_start)
if line_start == -1:
    actual_line_start = 0
else:
    actual_line_start = line_start + 1

print(f"Line start position: {actual_line_start}")
print(f"Characters from line start: {repr(full_content[actual_line_start:actual_line_start+50])}")

# Now let's see what the tokenizer produces for this section
print("\n=== TOKENIZER FOR PIPELINE SECTION ===")
tokenizer = Tokenizer(full_content)
tokens = tokenizer.tokenize()
filtered_tokens = [t for t in tokens if t.type not in ("NEWLINE", "COMMENT", "SKIP")]

# Find tokens around our section
for i, token in enumerate(filtered_tokens):
    if token.start >= section_start - 50 and token.start <= section_start + 100:
        line_start_for_token = full_content.rfind('\n', 0, token.start)
        if line_start_for_token == -1:
            token_line_start = 0
        else:
            token_line_start = line_start_for_token + 1
        print(f"Token {i}: {token.type} = {repr(token.value)} at {token.start}-{token.end}, line_start={token_line_start}")

# Test what happens when we format this with the current logic
print(f"\n=== CURRENT FORMATTING LOGIC ===")
extracted_text = full_content[actual_line_start:section_end]
print(f"Extracted text: {repr(extracted_text)}")

pipeline_lines = [f"  {line.strip()}" for line in extracted_text.split('\n') if line.strip()]
formatted_result = '\n'.join(pipeline_lines)
print(f"Formatted result: {repr(formatted_result)}")

print("\nFormatted lines breakdown:")
for i, line in enumerate(formatted_result.split('\n')):
    spaces = len(line) - len(line.lstrip())
    print(f"  Line {i}: {spaces} spaces: {repr(line)}")
