#!/usr/bin/env python3

import os

# The ordered list of test module filenames
module_files = [
    "lists.enzo",
    "math.enzo",
    "tables.enzo",
    "text.enzo",
    "vars.enzo",
    "functions.enzo"
]

base_dir = os.path.dirname(os.path.abspath(__file__))
modules_dir = os.path.join(base_dir, "test-modules")
golden_dir = os.path.join(base_dir, "golden-files")
output_file = os.path.join(base_dir, "combined-tests.enzo")
golden_output_file = os.path.join(base_dir, "combined-tests.golden.enzo")

# Combine test modules
def combine_files(file_list, input_dir, output_path, suffix=""):
    with open(output_path, "w") as out:
        for fname in file_list:
            # For golden files, replace .enzo with .golden.enzo
            in_fname = fname if not suffix else fname.replace(".enzo", suffix)
            path = os.path.join(input_dir, in_fname)
            if not os.path.exists(path):
                print(f"⚠️  Warning: File not found: {in_fname}")
                continue
            with open(path, "r") as f:
                out.write(f.read().rstrip() + "\n\n")

combine_files(module_files, modules_dir, output_file)
combine_files(module_files, golden_dir, golden_output_file, suffix=".golden.enzo")

print(f"✅ Combined test file regenerated at: {output_file}")
print(f"✅ Combined golden file regenerated at: {golden_output_file}")