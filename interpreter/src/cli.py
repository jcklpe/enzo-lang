import sys
import re
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

def read_statement(stdin, interactive):
    buffer = []
    depth = 0
    while True:
        if interactive:
            prompt = "enzo> " if not buffer else "...   "
            line = input(prompt)
        else:
            line = stdin.readline()
            if not line:
                break
            line = line.rstrip('\n')

        # Skip blank/comment lines unless already in a statement
        if not line.strip() and not buffer:
            continue
        if line.strip().startswith('//') and not buffer:
            continue

        buffer.append(line)

        # Count parens/brackets/braces to handle multi-line
        openers = line.count('(') + line.count('{') + line.count('[')
        closers = line.count(')') + line.count('}') + line.count(']')
        depth += openers - closers

        # Check for semicolon at end of any line and balanced depth
        if depth == 0 and ';' in line:
            break
    return '\n'.join(buffer) if buffer else None

def main() -> None:
    interactive = sys.stdin.isatty()

    if interactive:
        print("enzo repl — ctrl-D to exit")

    while True:
        try:
            stmt = read_statement(sys.stdin, interactive)
            if stmt is None:
                break
            line = stmt
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