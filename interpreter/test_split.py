#!/usr/bin/env python3

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

def test_split_statements():
    # Test the split_statements function with the third test case
    def split_statements(lines):
        # Split a list of lines into complete statements (respecting nesting)
        stmts = []
        buffer = []
        paren_depth = 0
        brace_depth = 0
        bracket_depth = 0
        for line in lines:
            stripped = line.rstrip('\n')
            print(f"Processing line: {repr(stripped)}, current paren_depth: {paren_depth}")
            # Skip blank/comment lines unless already in a statement
            if not stripped and not buffer:
                continue
            if stripped.strip().startswith('//=') and not buffer:
                stmts.append([stripped])
                continue
            if stripped.strip().startswith('//') and not buffer:
                continue
            # Update depths
            for char in stripped:
                if char == '(':
                    paren_depth += 1
                elif char == ')':
                    paren_depth -= 1
                elif char == '{':
                    brace_depth += 1
                elif char == '}':
                    brace_depth -= 1
                elif char == '[':
                    bracket_depth += 1
                elif char == ']':
                    bracket_depth -= 1
            buffer.append(stripped)
            print(f"After processing: paren_depth={paren_depth}, brace_depth={brace_depth}, bracket_depth={bracket_depth}, has_semicolon={';' in stripped}")
            if paren_depth <= 0 and brace_depth <= 0 and bracket_depth <= 0 and ';' in stripped:
                print(f"BREAKING: Adding statement: {buffer}")
                stmts.append(buffer)
                buffer = []
            else:
                print(f"CONTINUE: buffer now: {buffer}")
        if buffer:
            print(f"FINAL: Adding remaining buffer: {buffer}")
            stmts.append(buffer)
        return stmts

    # Test case 3 content
    lines = [
        "($z: 101;",
        "$t: 102;",
        "return(($z + $t));",
        ");"
    ]

    print("Testing split_statements with third test case:")
    print("Input lines:", lines)
    print()

    result = split_statements(lines)
    print()
    print("Result:")
    for i, stmt in enumerate(result):
        print(f"Statement {i}: {stmt}")

if __name__ == "__main__":
    test_split_statements()
