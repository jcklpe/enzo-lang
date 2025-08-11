#!/usr/bin/env python3

# Debug script to check the raw pipeline text extraction

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.enzo_parser.tokenizer import Tokenizer
from src.enzo_parser.parser import Parser

# Test the specific pipeline that's causing issues
test_code = '''$list-pipe
then ($this contains 4) :> $contains-four;'''

print("Original test code:")
print(repr(test_code))
print()

print("Original test code formatted:")
print(test_code)
print()

# Parse and find the pipeline start position
tokens = Tokenizer(test_code).tokenize()
tokens = [t for t in tokens if t.type not in ("NEWLINE", "COMMENT", "SKIP")]

print("Tokens:")
for i, token in enumerate(tokens):
    print(f"  {i}: {token.type} = '{token.value}' (start={token.start}, end={token.end})")
print()

# Find the variable token that starts the pipeline
statement_start_pos = 0
for i in range(len(tokens)):
    token = tokens[i]
    if token.type == "KEYNAME" and token.value.startswith("$"):
        statement_start_pos = token.start
        print(f"Found pipeline start at position {statement_start_pos}")
        break

# Find the semicolon
end_pos = len(test_code)
for token in tokens:
    if token.type == "SEMICOLON":
        end_pos = token.end
        print(f"Found semicolon end at position {end_pos}")
        break

# Extract the pipeline text
pipeline_text = test_code[statement_start_pos:end_pos]
print(f"Raw pipeline text: {repr(pipeline_text)}")
print()

print("Raw pipeline text formatted:")
print(pipeline_text)
print()

# Show how it's currently being formatted
pipeline_lines = [f"  {line.strip()}" for line in pipeline_text.split('\n') if line.strip()]
multi_line_context = '\n'.join(pipeline_lines)
print("Current formatting result:")
print(repr(multi_line_context))
print()
print("Current formatting result formatted:")
print(multi_line_context)
