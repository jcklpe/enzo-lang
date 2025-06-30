#!/usr/bin/env python3

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

def debug_split_statements():
    # Test the split_statements function with the error recovery case
    def split_statements(lines):
        # Split a list of lines into complete statements (respecting nesting)
        stmts = []
        buffer = []
        paren_depth = 0
        brace_depth = 0
        bracket_depth = 0
        for line in lines:
            stripped = line.rstrip('\n')
            print(f"Processing line: {repr(stripped)}")
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
            print(f"  Depths: paren={paren_depth}, brace={brace_depth}, bracket={bracket_depth}")
            print(f"  Has semicolon: {';' in stripped}")
            if paren_depth <= 0 and brace_depth <= 0 and bracket_depth <= 0 and ';' in stripped:
                print(f"  -> Statement complete: {buffer}")
                stmts.append(buffer)
                buffer = []
            else:
                print(f"  -> Continuing statement: {buffer}")
        if buffer:
            print(f"Final buffer: {buffer}")
            stmts.append(buffer)
        return stmts

    # Test with the error recovery content
    lines = [
        "//= Test error recovery",
        "(1 + 2                 // error: unmatched parenthesis",
        "(1 + 2;                 // error: unmatched parenthesis"
    ]

    print("Input lines:")
    for i, line in enumerate(lines):
        print(f"  {i}: {repr(line)}")
    print()

    result = split_statements(lines)
    print("Split statements:")
    for i, stmt in enumerate(result):
        print(f"  Statement {i}: {stmt}")

if __name__ == "__main__":
    debug_split_statements()
