#!/usr/bin/env python3

# Debug script to check token positions and pipeline start position tracking

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.enzo_parser.tokenizer import Tokenizer

# Read the actual test file and find the problematic pipeline
with open('tests/test-modules/conditional-flow.enzo', 'r') as f:
    content = f.read()

print("Full file content around the pipeline:")
lines = content.split('\n')
pipeline_line_num = None
for i, line in enumerate(lines):
    if line.strip() == '$list-pipe' and i+1 < len(lines) and 'then' in lines[i+1]:
        pipeline_line_num = i
        print(f"Found pipeline starting at line {i+1}")
        # Show context around this line
        for j in range(max(0, i-2), min(len(lines), i+5)):
            marker = ">>> " if j == i or j == i+1 else "    "
            print(f"{marker}Line {j+1}: {repr(lines[j])}")
        break

if pipeline_line_num is not None:
    # Extract just the pipeline section and a bit before
    start_context = max(0, pipeline_line_num - 1)
    end_context = min(len(lines), pipeline_line_num + 3)
    context_lines = lines[start_context:end_context]
    context_text = '\n'.join(context_lines)

    print(f"\nContext text from line {start_context+1} to {end_context}:")
    print(repr(context_text))

    # Tokenize this context
    tokens = Tokenizer(context_text).tokenize()
    tokens = [t for t in tokens if t.type not in ("NEWLINE", "COMMENT", "SKIP")]

    print(f"\nTokens in context:")
    for i, token in enumerate(tokens):
        print(f"  {i}: {token.type} = {repr(token.value)} (start={token.start}, end={token.end})")

    # Find the $list-pipe token
    list_pipe_token = None
    for token in tokens:
        if token.value == '$list-pipe' and token.type == 'KEYNAME':
            list_pipe_token = token
            break

    if list_pipe_token:
        print(f"\n$list-pipe token found at position {list_pipe_token.start}-{list_pipe_token.end}")
        print(f"Text at that position: {repr(context_text[list_pipe_token.start:list_pipe_token.end])}")

        # Check what character is at position list_pipe_token.start
        if list_pipe_token.start > 0:
            print(f"Character before $list-pipe: {repr(context_text[list_pipe_token.start-1])}")
        print(f"Characters around $list-pipe:")
        start_check = max(0, list_pipe_token.start - 5)
        end_check = min(len(context_text), list_pipe_token.end + 5)
        print(f"  {repr(context_text[start_check:end_check])}")

        # Check if there are leading spaces
        line_start = context_text.rfind('\n', 0, list_pipe_token.start)
        if line_start == -1:
            line_start = 0
        else:
            line_start += 1  # Skip the newline

        line_text = context_text[line_start:list_pipe_token.end]
        print(f"Line containing $list-pipe: {repr(line_text)}")
        print(f"Leading whitespace: {repr(line_text[:list_pipe_token.start-line_start])}")

        # Calculate what the position should be for the start of the line
        expected_start = line_start
        print(f"Expected pipeline start position: {expected_start}")
        print(f"Actual token start position: {list_pipe_token.start}")

        if expected_start != list_pipe_token.start:
            print(f"MISMATCH! Expected {expected_start}, got {list_pipe_token.start}")
            print(f"Difference: {list_pipe_token.start - expected_start} characters")
