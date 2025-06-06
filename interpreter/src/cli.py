import sys
from src.parser       import parse
from src.evaluator    import eval_ast
from src.ast_helpers  import Table, format_val
from src.parse_errors import format_parse_error
from lark import UnexpectedToken, UnexpectedInput, UnexpectedCharacters

def say(val):
    print(val)

def print_enzo_error(msg):
    import sys
    # ANSI codes
    RED = "\033[91m"
    RESET = "\033[0m"
    BLACK_BG = "\033[40m"
    WHITE = "\033[97m"

    # Split into lines
    lines = msg.split('\n')
    if not lines:
        print(RED + msg + RESET)
        return

    # First line: red (the error summary)
    print(f"{RED}{lines[0]}{RESET}", file=sys.stderr)
    # Remaining lines: treat as code block (if present)
    for code_line in lines[1:]:
        # Only print non-empty lines, and add code-like background
        if code_line.strip():
            print(f"{BLACK_BG}{WHITE}{code_line.rstrip()}{RESET}", file=sys.stderr)


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
        except (UnexpectedToken, UnexpectedInput, UnexpectedCharacters) as e:
            print_enzo_error("error: " + format_parse_error(e, src=line))
        except Exception as e:
            print("error:", e)