#!/usr/bin/env python3
import subprocess
import difflib
import os
import sys

# Adjust path if run from project root, so 'src' is on the import path
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = os.path.join(SCRIPT_DIR, "src")
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

try:
    from color_helpers import color_error, color_info, color_diff
except ImportError:
    # Fallback: import from src.color_helpers if running from inside interpreter/
    from src.color_helpers import color_error, color_info, color_diff

def usage():
    print(color_error(f"Usage: {sys.argv[0]} [module_name]"))
    print(color_error("  If no module_name is given, runs combined-tests."))
    print(color_error("  Else, runs tests/test-modules/<module_name>.enzo against tests/golden-files/<module_name>.golden.enzo"))
    sys.exit(1)

def get_test_and_golden(module=None):
    if module is None:
        test_file   = os.path.join("tests", "combined-tests.enzo")
        golden_file = os.path.join("tests", "combined-tests.golden.enzo")
    else:
        test_file   = os.path.join("tests", "test-modules", f"{module}.enzo")
        golden_file = os.path.join("tests", "golden-files", f"{module}.golden.enzo")
    return test_file, golden_file

def main():
    # Support help flags
    if len(sys.argv) > 1 and sys.argv[1] in {"-h", "--help"}:
        usage()

    module = sys.argv[1] if len(sys.argv) > 1 else None
    test_file, golden_file = get_test_and_golden(module)

    if not os.path.exists(test_file):
        print(color_error(f"❗ Test file not found: {test_file}"))
        usage()
    if not os.path.exists(golden_file):
        print(color_error(f"❗ Golden file not found: {golden_file}"))
        usage()

    # Run the interpreter
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
    else:
        print(color_error(f"❌ {test_file} does NOT match golden file.\n"))
        for line in difflib.unified_diff(
            expected.splitlines(),
            actual.splitlines(),
            fromfile="expected",
            tofile="actual",
            lineterm=""
        ):
            if line.startswith('@@'):
                print()  # blank line before each new diff hunk
            print(color_diff(line))

if __name__ == "__main__":
    main()
