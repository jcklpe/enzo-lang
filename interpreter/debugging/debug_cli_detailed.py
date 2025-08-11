#!/usr/bin/env python3

import sys
sys.path.append('src')

def debug_cli_path():
    statement = '''If $status-if,
  "Ready!"; // should print "Ready!"
end;'''

    print("=== DEBUGGING CLI PATH ===")
    print(f"Statement:\n{repr(statement)}")

    # Mimic CLI logic
    stmt_lines = statement.strip().split('\n')
    print(f"Statement lines: {stmt_lines}")

    # Check condition like CLI does
    condition1 = all(';' in line for line in stmt_lines)
    condition2 = len(stmt_lines) > 1
    condition3 = not any(line.strip().startswith(('(', '[', '{')) for line in stmt_lines)
    condition4 = not any('then (' in line for line in stmt_lines)
    condition5 = not any(any(keyword in line for keyword in ['If ', 'Else', 'end;']) for line in stmt_lines)

    print(f"Condition 1 (all have ;): {condition1}")
    print(f"Condition 2 (multiple lines): {condition2}")
    print(f"Condition 3 (no special starts): {condition3}")
    print(f"Condition 4 (no then): {condition4}")
    print(f"Condition 5 (no control flow): {condition5}")

    final_condition = condition1 and condition2 and condition3 and condition4 and condition5
    print(f"Final condition (line-by-line): {final_condition}")

    if final_condition:
        print("\n=== WOULD PROCESS LINE BY LINE ===")
        for line in stmt_lines:
            line = line.strip()
            if not line:
                continue
            # Strip inline comments (for code lines only)
            if '//' in line:
                line = line.split('//', 1)[0].rstrip()
            if not line:
                continue
            print(f"Processing line: {repr(line)}")
    else:
        print("\n=== WOULD PROCESS AS BLOCK ===")
        print("Using parse_program or parse")

if __name__ == "__main__":
    debug_cli_path()
