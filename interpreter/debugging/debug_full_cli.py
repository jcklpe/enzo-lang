#!/usr/bin/env python3

import sys
sys.path.append('src')

from src.enzo_parser.parser import parse_program, parse
from src.evaluator import eval_ast

def debug_full_cli_simulation():
    # Simulate the exact CLI behavior for the first test

    # Step 1: Read file and split into test blocks (like CLI does)
    with open('tests/test-modules/control-flow.enzo', 'r') as f:
        content = f.read()

    # Split by //= delimiters
    import re
    delim_pattern = re.compile(r'^//= *(.*)$', re.MULTILINE)
    matches = list(delim_pattern.finditer(content))

    # Get first test block content
    first_match = matches[0]
    if len(matches) > 1:
        first_block_content = content[first_match.end():matches[1].start()].strip()
    else:
        first_block_content = content[first_match.end():].strip()

    print("=== CLI SIMULATION ===")
    print(f"First block content:\n{repr(first_block_content)}")

    # Step 2: Split into statements (like CLI does)
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
        print(f"Statement {i}: {repr(stmt)}")

    # Step 3: Process each statement (like CLI does)
    env = {}

    for i, statement in enumerate(statements):
        print(f"\n=== PROCESSING STATEMENT {i} ===")
        print(f"Statement: {repr(statement)}")

        # Check CLI logic
        is_multiline = '\n' in statement
        print(f"Is multiline: {is_multiline}")

        # Strip comments for single-line statements
        if not is_multiline and '//' in statement:
            statement = statement.split('//', 1)[0].rstrip()
            print(f"After comment stripping: {repr(statement)}")

        if not statement:
            print("Empty statement, skipping")
            continue

        try:
            # Use CLI logic for choosing parser
            if '\n' in statement or ';' in statement.rstrip(';'):
                print("Using parse_program")
                result = eval_ast(parse_program(statement), value_demand=True, env=env)
            else:
                print("Using parse")
                result = eval_ast(parse(statement), value_demand=True, env=env)

            print(f"SUCCESS: {result}")
            if result is not None:
                # Simulate CLI output
                if isinstance(result, list):
                    for item in result:
                        if item is not None:
                            print(f"OUTPUT: {item}")
                else:
                    print(f"OUTPUT: {result}")
        except Exception as e:
            print(f"ERROR: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    debug_full_cli_simulation()
