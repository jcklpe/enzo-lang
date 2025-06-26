#!/usr/bin/env python3
import subprocess
import difflib
import os
import sys
import re
import pathlib

# Use these for diff output instead of '+' and '-'
EXPECTED_MARK = '✔'
ACTUAL_MARK = '✖'

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
    #Returns a list of (title, block_lines_list)
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

def color_diff_symbol_line(line):
    # Color lines based on our new markers
    if not sys.stdout.isatty():
        return line
    if line.startswith(ACTUAL_MARK):
        return f"\033[91m{line}\033[0m"  # Red for actual/failing
    if line.startswith(EXPECTED_MARK):
        return f"\033[92m{line}\033[0m"  # Green for expected/passing
    if line.startswith('@@'):
        return f"\033[93;1m{line}\033[0m"
    return line

def main():
    if len(sys.argv) > 1 and sys.argv[1] in {"-h", "--help"}:
        print("Usage: ./run-tests.py [module_name]")
        sys.exit(1)

    module = sys.argv[1] if len(sys.argv) > 1 else None

    # --- NEW: Regenerate combined-tests.enzo if running the full suite ---
    if not module:
        regen_script = os.path.join(SCRIPT_DIR, "tests", "regen-combined-tests.py")
        if not os.path.exists(regen_script):
            print(color_error(f"❗ regen-combined-tests.py not found at {regen_script}"))
            sys.exit(1)
        result = subprocess.run(
            [sys.executable, regen_script],
            cwd=os.path.join(SCRIPT_DIR, "tests"),
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(color_error("❗ Failed to regenerate combined-tests.enzo:"))
            print(result.stdout)
            print(result.stderr)
            sys.exit(1)

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
    print(color_expected_header('✔ correct expected outcome'))
    print(color_actual_header('✖ failing actual outcome'))

    fail_count = 0
    for i in range(num_blocks):
        title, exp_lines = expected_blocks[i]
        _, act_lines = actual_blocks[i]
        # Compare ignoring leading/trailing whitespace
        if [l.rstrip() for l in exp_lines] != [l.rstrip() for l in act_lines]:
            fail_count += 1
            print()
            print(color_block_title(f"//= {title}"))
            diff = difflib.unified_diff(
                exp_lines,
                act_lines,
                fromfile="actual",
                tofile="expected",
                lineterm=""
            )
            for line in diff:
                # Swap -/+ for ✔/✖ for output and coloring
                if line.lstrip('-+ ').startswith(f"//= {title}"):
                    continue
                if line.startswith('---') or line.startswith('+++'):
                    continue
                if line.startswith('+'):
                    line = ACTUAL_MARK + line[1:]
                    print(color_diff_symbol_line(line))
                elif "Syntax error:" in line or "Expected one of:" in line:
                    print(color_red(line))
                elif line.startswith('-'):
                    line = EXPECTED_MARK + line[1:]
                    print(color_diff_symbol_line(line))
                elif line.startswith('@@'):
                    print(color_diff(line))
                else:
                    print(line)
    print("\n==================== TEST SUMMARY ====================")
    print(f"Failing test blocks: {fail_count} / {num_blocks}")
    if fail_count == 0:
        print(color_info("All test blocks passed!"))
    else:
        print(color_error(f"{fail_count} test blocks failed."))

    # --- RUN DEBUG MODULE AT THE END OF TEST OUTPUT ---
    print("\n" + "=" * 60)
    print("🟡  [debug-module.py] Running optional debug diagnostics...\n")
    subprocess.run([sys.executable, "tests/debug_module.py"], check=False)
    print("=" * 60)
    print("🟡  [debug-module.py] Debug diagnostics complete.\n")

if __name__ == "__main__":
    main()
