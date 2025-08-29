#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.cli import split_statements

# Check how the else-if test case is split into statements
test_lines = [
    '$level-scope: 1;',
    'If $level-scope is 0, (',
    '    $msg-scope: "Level 0";',
    '), Else if $level-scope is 1, (',
    '    $msg-scope: "Level 1"; // This shadows any outer $msg and is local to this block.',
    '    "In Else If: <$msg-scope>"; // Prints "Level 1"',
    '), Else, (',
    '    $msg-scope: "Other Level";',
    ');',
    '$msg-scope; // error: undefined variable (each $msg was local to its own conditional block)',
    ''
]

stmts = split_statements(test_lines)

print("=== Statement Blocks for else-if test ===")
for i, stmt_lines in enumerate(stmts):
    print(f"\nBlock {i}:")
    print(f"  Lines: {stmt_lines}")
    statement = '\n'.join(stmt_lines).strip()
    print(f"  Statement: {repr(statement)}")

    # Check if this would trigger single-line processing
    is_multiline = '\n' in statement
    print(f"  Is multiline: {is_multiline}")

    if 'msg-scope' in statement and 'error' in statement:
        print(f"  *** THIS IS THE ERROR LINE ***")
