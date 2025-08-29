#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.cli import split_statements

# Read the conditional shadowing test file and see how it's split into statements
with open('tests/test-modules/conditional-shadowing.enzo') as f:
    lines = f.readlines()

stmts = split_statements(lines)

print("=== Statement Blocks ===")
for i, stmt_lines in enumerate(stmts):
    print(f"\nBlock {i}:")
    print(f"  Lines: {stmt_lines}")
    statement = '\n'.join(stmt_lines).strip()
    print(f"  Statement: {repr(statement)}")

    # Check if this would trigger single-line processing
    is_multiline = '\n' in statement
    has_semicolons = all(';' in line for line in stmt_lines) and len(stmt_lines) > 1
    print(f"  Is multiline: {is_multiline}")
    print(f"  Has semicolons: {has_semicolons}")

    if '$z-local' in statement:
        print(f"  *** THIS IS THE FAILING BLOCK ***")

        # Check what the comment stripping would do
        if not is_multiline and '//' in statement:
            stripped = statement.split('//', 1)[0].rstrip()
            print(f"  Would be stripped to: {repr(stripped)}")
        else:
            print(f"  Would NOT be stripped")
