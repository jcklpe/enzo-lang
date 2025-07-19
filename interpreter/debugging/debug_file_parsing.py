#!/usr/bin/env python3

import sys
sys.path.append('src')

def debug_file_parsing():
    # Read the actual test file
    with open('tests/test-modules/control-flow.enzo', 'r') as f:
        content = f.read()

    print("=== DEBUGGING FILE PARSING ===")

    # Split by //= delimiters like the CLI does
    import re

    # Split into statement blocks
    delim_pattern = re.compile(r'^//= *(.*)$', re.MULTILINE)
    matches = list(delim_pattern.finditer(content))

    print(f"Found {len(matches)} test blocks")

    if matches:
        # Get the first test block
        first_match = matches[0]
        if len(matches) > 1:
            first_block_content = content[first_match.end():matches[1].start()].strip()
        else:
            first_block_content = content[first_match.end():].strip()

        print(f"\nFirst test block:")
        print(f"Title: {first_match.group(1)}")
        print(f"Content:\n{repr(first_block_content)}")

        # Split into statements
        statements = []
        current_statement = []

        for line in first_block_content.split('\n'):
            line = line.rstrip()
            if line == "":
                if current_statement:
                    statements.append('\n'.join(current_statement))
                    current_statement = []
            else:
                current_statement.append(line)

        if current_statement:
            statements.append('\n'.join(current_statement))

        print(f"\nSplit into {len(statements)} statements:")
        for i, stmt in enumerate(statements):
            print(f"Statement {i}:")
            print(f"{repr(stmt)}")
            print()

if __name__ == "__main__":
    debug_file_parsing()
