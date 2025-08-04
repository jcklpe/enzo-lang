#!/usr/bin/env python3

# Debug the exact position tracking logic

context_text = '\n$list-pipe\nthen ($this contains 4) :> $contains-four;  // error: comparison word in pipeline\n'

print("Context text:", repr(context_text))

# Simulate finding the $list-pipe token at position 1
token_start = 1

# Find the start of the line containing this token
line_start = context_text.rfind('\n', 0, token_start)
print(f"Line start search result: {line_start}")

if line_start == -1:
    statement_start_pos = 0  # Beginning of file
else:
    statement_start_pos = line_start + 1  # After the newline

print(f"Statement start position: {statement_start_pos}")

# Find end position (semicolon)
end_pos = context_text.find(';') + 1
print(f"End position: {end_pos}")

# Extract the pipeline text
pipeline_text = context_text[statement_start_pos:end_pos]
print(f"Pipeline text: {repr(pipeline_text)}")

# Apply the formatting logic
pipeline_lines = [f"  {line.strip()}" for line in pipeline_text.split('\n') if line.strip()]
formatted = '\n'.join(pipeline_lines)
print(f"Formatted result: {repr(formatted)}")
print("Formatted display:")
print(formatted)
