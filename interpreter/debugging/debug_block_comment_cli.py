#!/usr/bin/env python3
import sys
import os
sys.path.append('..')

# Import the CLI's statement splitting logic
from src.cli import split_statements, process_includes

# Read the test file exactly like the CLI does
filename = "/Users/aslan/work/enzo-lang/interpreter/tests/test-modules/block-comment.enzo"
with open(filename) as f:
    lines = f.readlines()

lines = list(process_includes(lines, base_dir=os.path.dirname(os.path.abspath(filename))))
stmts = split_statements(lines)

print("=== STATEMENTS EXTRACTED BY CLI ===")
for i, stmt_lines in enumerate(stmts):
    statement = '\n'.join(stmt_lines).strip()
    print(f"\nStatement {i+1}:")
    print(f"Raw: {repr(statement)}")
    print(f"Content:\n{statement}")
    print("-" * 40)

# Now let's try to tokenize each statement individually
print("\n=== TOKENIZING EACH STATEMENT ===")
from src.enzo_parser.tokenizer import Tokenizer

for i, stmt_lines in enumerate(stmts):
    statement = '\n'.join(stmt_lines).strip()
    if not statement or statement.startswith('//='):
        print(f"Statement {i+1}: Skipping (empty or comment)")
        continue

    print(f"\nTokenizing statement {i+1}:")
    print(f"Statement: {repr(statement)}")
    try:
        tokenizer = Tokenizer(statement)
        tokens = tokenizer.tokenize()
        print(f"Success: {len(tokens)} tokens")
        for token in tokens:
            print(f"  {token}")
    except Exception as e:
        print(f"ERROR: {e}")
        print(f"Statement was: {repr(statement)}")
