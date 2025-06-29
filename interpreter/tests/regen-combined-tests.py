#!/usr/bin/env python3

import os

# Normalize golden files before combining
try:
    from tests.normalize_golden_files import normalize_golden_files
    normalize_golden_files()
except Exception as e:
    print(f"Warning: Could not normalize golden files: {e}")

# The ordered list of test module filenames
module_files = [
    "vars.enzo",
    "lists.enzo",
    "math.enzo",
    "tables.enzo",
    "text.enzo",
    "functions.enzo",
    "misc.enzo"
]

base_dir = os.path.dirname(os.path.abspath(__file__))
modules_dir = os.path.join(base_dir, "test-modules")
golden_dir = os.path.join(base_dir, "golden-files")
output_file = os.path.join(base_dir, "combined-tests.enzo")
golden_output_file = os.path.join(base_dir, "combined-tests.golden.enzo")

# Combine test modules
def combine_files(file_list, input_dir, output_path, suffix=""):
    contents = []
    for fname in file_list:
        in_fname = fname if not suffix else fname.replace(".enzo", suffix)
        path = os.path.join(input_dir, in_fname)
        if not os.path.exists(path):
            continue
        with open(path, "r") as f:
            # Strip all trailing newlines from the file
            content = f.read().rstrip('\n')
            contents.append(content)
    # Join with exactly two newlines between blocks, but no trailing newlines at the end
    combined = '\n\n'.join(contents)
    # Optionally, add a single newline at the end for POSIX compliance
    with open(output_path, "w") as out:
        out.write(combined)
        out.write('\n')

combine_files(module_files, modules_dir, output_file)
combine_files(module_files, golden_dir, golden_output_file, suffix=".golden.enzo")

print(f"✅ Combined test file regenerated at: {output_file}")
print(f"✅ Combined golden file regenerated at: {golden_output_file}")