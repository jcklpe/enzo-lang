#!/usr/bin/env python3

import sys
sys.path.append('src')

# Debug the CLI statement splitting logic

def debug_statement_splitting():
    statement = '''If $status-if,
  "Ready!";
end;'''

    print("=== DEBUGGING STATEMENT SPLITTING ===")
    print(f"Statement:\n{statement}")

    stmt_lines = statement.strip().split('\n')
    print(f"\nStatement lines: {stmt_lines}")

    # Check the condition
    has_semicolons = [';' in line for line in stmt_lines]
    print(f"Has semicolons: {has_semicolons}")
    print(f"All have semicolons: {all(';' in line for line in stmt_lines)}")

    starts_with_special = [line.strip().startswith(('(', '[', '{')) for line in stmt_lines]
    print(f"Starts with special: {starts_with_special}")
    print(f"Any start with special: {any(line.strip().startswith(('(', '[', '{')) for line in stmt_lines)}")

    has_then = ['then (' in line for line in stmt_lines]
    print(f"Has 'then (': {has_then}")
    print(f"Any have 'then (': {any('then (' in line for line in stmt_lines)}")

    # Check control flow keywords
    control_keywords = ['If ', 'Else', 'end;']
    has_control_flow = [any(keyword in line for keyword in control_keywords) for line in stmt_lines]
    print(f"Has control flow: {has_control_flow}")
    print(f"Any have control flow: {any(any(keyword in line for keyword in control_keywords) for line in stmt_lines)}")

    # Final condition
    condition = (all(';' in line for line in stmt_lines) and len(stmt_lines) > 1 and
                not any(line.strip().startswith(('(', '[', '{')) for line in stmt_lines) and
                not any('then (' in line for line in stmt_lines) and
                not any(any(keyword in line for keyword in control_keywords) for line in stmt_lines))

    print(f"\nFinal condition result: {condition}")
    print("Should process line by line:", condition)

if __name__ == "__main__":
    debug_statement_splitting()
