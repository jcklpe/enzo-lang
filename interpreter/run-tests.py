#!/usr/bin/env python3
import subprocess
import difflib
import os
import sys
import re

# Adjust path if run from project root, so 'src' is on the import path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = os.path.join(SCRIPT_DIR, "src")
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

try:
    from color_helpers import (
        color_error,
        color_info,
        color_diff,
        color_actual_header,
        color_expected_header,
        color_block_title,
        color_red,
    )
except ImportError:
    from src.color_helpers import (
        color_error,
        color_info,
        color_diff,
        color_actual_header,
        color_expected_header,
        color_block_title,
        color_red,
    )

# Block delimiter for titles
DELIM_RE = re.compile(r'^//= *(.*)$', re.MULTILINE)

def split_blocks(text):
    """
    Returns a list of (title, block_lines_list)
    """
    matches = list(DELIM_RE.finditer(text))
    if not matches:
        # Fallback: no block delimiters found, return the whole file as one unnamed block
        return [("", text.splitlines())]
    blocks = []
    for i, match in enumerate(matches):
        start = match.end()
        end = matches[i+1].start() if i+1 < len(matches) else len(text)
        title = match.group(1).strip()
        # Get block lines (without the //= line itself)
        lines = text[start:end].splitlines()
        # Remove blank lines at the start (if any)
        while lines and lines[0].strip() == "":
            lines = lines[1:]
        blocks.append((title, lines))
    return blocks

def color_actual_line_override(line):
    # Green for additions
    if not sys.stdout.isatty():
        return line
    if line.startswith('+'):
        return f"\033[92m{line}\033[0m"  # Green for additions
    if line.startswith('-'):
        return f"\033[91m{line}\033[0m"  # Red for deletions
    if line.startswith('@@'):
        return f"\033[93;1m{line}\033[0m"
    return line

def main():
    if len(sys.argv) > 1 and sys.argv[1] in {"-h", "--help"}:
        print("Usage: ./run-tests.py [module_name]")
        sys.exit(1)

    module = sys.argv[1] if len(sys.argv) > 1 else None
    test_file = f"tests/test-modules/{module}.enzo" if module else "tests/combined-tests.enzo"
    golden_file = f"tests/golden-files/{module}.golden.enzo" if module else "tests/combined-tests.golden.enzo"

    if not os.path.exists(test_file):
        print(color_error(f"❗ Test file not found: {test_file}"))
        sys.exit(1)
    if not os.path.exists(golden_file):
        print(color_error(f"❗ Golden file not found: {golden_file}"))
        sys.exit(1)

    proc = subprocess.run(
        ["poetry", "run", "enzo", test_file],
        capture_output=True,
        text=True
    )

    actual = proc.stdout.rstrip("\n")
    with open(golden_file) as f:
        expected = f.read().rstrip("\n")

    if actual == expected:
        print(color_info(f"✅ {test_file} matches golden file."))
        sys.exit(0)

    print(color_error(f"❌ {test_file} does NOT match golden file.\n"))

    # Split into blocks by //=
    actual_blocks = split_blocks(actual)
    expected_blocks = split_blocks(expected)
    num_blocks = min(len(actual_blocks), len(expected_blocks))

    # Print diff header only once at top
    print(color_expected_header('--- actual'))
    print(color_actual_header('+++ expected'))

    for i in range(num_blocks):
        title, exp_lines = expected_blocks[i]
        _, act_lines = actual_blocks[i]
        # Compare ignoring leading/trailing whitespace
        if [l.rstrip() for l in exp_lines] != [l.rstrip() for l in act_lines]:
            print()
            print(color_block_title(f"//= {title}"))
            diff = difflib.unified_diff(
                act_lines,
                exp_lines,
                fromfile="actual",
                tofile="expected",
                lineterm=""
            )
            for line in diff:
                if line.lstrip('-+ ').startswith(f"//= {title}"):
                    continue
                # Skip redundant headers
                if line.startswith('---') or line.startswith('+++'):
                    continue
                # Highlight Lark parse errors in red
                if "Syntax error:" in line or "Expected one of:" in line:
                    print(color_red(line))
                elif line.startswith('+'):
                    print(color_actual_line_override(line))
                elif line.startswith('-'):
                    print(color_diff(line))
                elif line.startswith('@@'):
                    print(color_diff(line))
                else:
                    print(line)

if __name__ == "__main__":
    main()
