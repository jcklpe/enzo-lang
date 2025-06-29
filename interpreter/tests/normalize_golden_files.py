import os

def normalize_golden_files():
    golden_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "golden-files")
    for fname in os.listdir(golden_dir):
        if fname.endswith(".golden.enzo"):
            path = os.path.join(golden_dir, fname)
            with open(path, "r") as f:
                content = f.read().rstrip('\n') + '\n'
            with open(path, "w") as f:
                f.write(content)
