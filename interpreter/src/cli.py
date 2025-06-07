import sys
import re
from src.parser       import parse
from src.evaluator    import eval_ast, InterpolationParseError
from src.ast_helpers  import Table, format_val
from src.parse_errors import format_parse_error
from lark import UnexpectedToken, UnexpectedInput, UnexpectedCharacters
from src.color_helpers import color_error, color_code

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
    while True:
        if interactive:
            prompt = "enzo> " if not buffer else "...   "
            try:
                line = input(prompt)
            except EOFError:
                break
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

        # If any semicolon is found, treat as end of statement
        if ';' in line:
            break

    return '\n'.join(buffer) if buffer else None

def main():
    interactive = sys.stdin.isatty()

    if interactive:
        print("enzo repl — ctrl-D to exit")

    # Process all input, line by line
    while True:
        stmt = None
        try:
            stmt = read_statement(sys.stdin, interactive)
        except (EOFError, KeyboardInterrupt):
            break

        if stmt is None:
            break

        line = stmt.strip()
        if not line:
            continue
        if line.startswith("//"):
            continue

        try:
            ast = parse(line)
            out = eval_ast(ast)
            if out is not None:
                if isinstance(out, list) or isinstance(out, (dict, Table)):
                    print(format_val(out))
                else:
                    print(out)
        except InterpolationParseError:
            print(color_error("error: parse error in interpolation"))
            print(color_code("    " + line))
            underline = "    " + " " * line.find("<") + "^"
            print(color_code(underline))
        except (UnexpectedToken, UnexpectedInput, UnexpectedCharacters) as e:
            fullmsg = format_parse_error(e, src=line)
            if "\n" in fullmsg:
                errline, context = fullmsg.split("\n", 1)
                print(color_error(errline))
                print(color_code(context))
            else:
                print(color_error(fullmsg))
        except Exception as e:
            print(color_error(f"error: {e}"))
            print(color_code("    " + line))
            print(color_code("    " + "^" * len(line)))
        # — CRITICAL FIX: after error or success, **continue the loop**
        # Don't break; keep processing all input!

if __name__ == "__main__":
    main()
