#!/usr/bin/env python3

import sys
sys.path.append("../src")

from src.enzo_parser.parser import Parser
from src.enzo_parser.tokenizer import Tokenizer

# Test the exact content from the test file
test_content = '''//= MULTI-STAGE PIPELINE WITH CONDITIONAL STEP ERROR
$list-pipe: [1,2,3,4];

$list-pipe
then ($this contains 4) :> $contains-four;  // error: comparison word in pipeline'''

print("=== DEBUGGING PIPELINE POSITION TRACKING ===")
print("Source content:")
lines = test_content.split('\n')
for i, line in enumerate(lines):
    print(f"Line {i}: {repr(line)}")

print(f"\nTotal source length: {len(test_content)}")

# Let's manually find where the pipeline statement starts
pipeline_start = test_content.find('$list-pipe\nthen')
print(f"Pipeline statement starts at index: {pipeline_start}")

# Find line start
line_start = test_content.rfind('\n', 0, pipeline_start)
if line_start == -1:
    actual_line_start = 0
else:
    actual_line_start = line_start + 1
print(f"Line start for pipeline would be: {actual_line_start}")

# Show what character is at that position
print(f"Character at line start: {repr(test_content[actual_line_start:actual_line_start+1])}")
print(f"Next few characters: {repr(test_content[actual_line_start:actual_line_start+20])}")

# Now let's see what the tokenizer produces
print("\n=== TOKENIZER OUTPUT ===")
tokenizer = Tokenizer(test_content)
tokens = tokenizer.tokenize()
filtered_tokens = [t for t in tokens if t.type not in ("NEWLINE", "COMMENT", "SKIP")]

for i, token in enumerate(filtered_tokens):
    print(f"Token {i}: {token.type} = {repr(token.value)} at positions {token.start}-{token.end}")

# Find the $list-pipe token that should start the pipeline
pipeline_var_tokens = [t for t in filtered_tokens if t.type == "KEYNAME" and t.value == "$list-pipe"]
print(f"\nFound {len(pipeline_var_tokens)} $list-pipe tokens:")
for i, token in enumerate(pipeline_var_tokens):
    print(f"  Token {i}: {repr(token.value)} at positions {token.start}-{token.end}")
    # Find line start for this token
    line_start = test_content.rfind('\n', 0, token.start)
    if line_start == -1:
        token_line_start = 0
    else:
        token_line_start = line_start + 1
    print(f"    Line start for this token: {token_line_start}")
    print(f"    Characters from line start: {repr(test_content[token_line_start:token_line_start+20])}")

print("\n=== PARSER TEST ===")
try:
    parser = Parser(test_content)
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
