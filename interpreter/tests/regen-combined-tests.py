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
output_file = os.path.join(base_dir, "combined-tests.enzo")

with open(output_file, "w") as out:
    for fname in module_files:
        path = os.path.join(modules_dir, fname)
        if not os.path.exists(path):
            print(f"⚠️  Warning: Module not found: {fname}")
            continue
        # Write a clear header to separate each module (helpful for navigation)
        out.write(f"//==================================================================\n")
        out.write(f"//= Included from: {fname}\n")
        out.write(f"//==================================================================\n")
        with open(path, "r") as f:
            out.write(f.read().rstrip() + "\n\n")

print(f"✅ Combined test file regenerated at: {output_file}")