import sys
from src.parser       import parse
from src.evaluator    import eval_ast
from src.ast_helpers  import Table, format_val

def say(val):
    print(val)

def main() -> None:
    interactive = sys.stdin.isatty()

    if interactive:
        print("enzo repl — ctrl-D to exit")

    while True:
        try:
            if interactive:
                line = input("enzo> ")
            else:
                line = sys.stdin.readline()
                if not line:  # EOF
                    break
                line = line.rstrip("\n")
        except (EOFError, KeyboardInterrupt):
            break

        stripped = line.strip()
        # Skip blank lines
        if not stripped:
            continue
        # Skip stand‐alone '//' comments
        if stripped.startswith("//"):
            continue

        try:
            ast = parse(line)
            out = eval_ast(ast)
            if out is not None:
                # pretty‐print lists or tables using format_val
                if isinstance(out, list) or isinstance(out, (dict, Table)):
                    print(format_val(out))
                else:
                    print(out)
        except Exception as e:
            print("error:", e)
