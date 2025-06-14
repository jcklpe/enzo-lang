#!/usr/bin/env python3
import os
import subprocess

TEST_MODULES_DIR = "tests/test-modules"
GOLDEN_FILES_DIR = "tests/golden-files"

def regenerate_golden(module_path):
    module_name = os.path.splitext(os.path.basename(module_path))[0]
    golden_path = os.path.join(GOLDEN_FILES_DIR, f"{module_name}.golden.enzo")
    # Run the interpreter
    result = subprocess.run(
        ["poetry", "run", "enzo", module_path],
        capture_output=True,
        text=True
    )
    with open(golden_path, "w") as f:
        f.write(result.stdout)
    print(f"✔️  Wrote {golden_path}")

def main():
    if not os.path.isdir(TEST_MODULES_DIR):
        print(f"Test modules dir not found: {TEST_MODULES_DIR}")
        return
    os.makedirs(GOLDEN_FILES_DIR, exist_ok=True)
    for fname in sorted(os.listdir(TEST_MODULES_DIR)):
        if fname.endswith(".enzo"):
            mod_path = os.path.join(TEST_MODULES_DIR, fname)
            regenerate_golden(mod_path)
    print("All golden files regenerated.")

if __name__ == "__main__":
    main()
