#!/usr/bin/env python3

import sys
import os

# Add the src directory to the path so we can import from it
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from cli import split_statements

# Test the problematic pipeline case
content = """$list-pipe: [1,2,3,4];

$list-pipe
then ($this contains 4) :> $contains-four;

$result: "done";"""

print("=== CONTENT ===")
print(repr(content))
print("\n=== SPLIT STATEMENTS ===")
statements = split_statements(content)
for i, stmt in enumerate(statements):
    print(f"Statement {i}:")
    print(repr(stmt))
    print()
