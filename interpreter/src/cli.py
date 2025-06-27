import sys
import re
import os
from src.enzo_parser.parser import parse  # Use new parser
from src.evaluator    import eval_ast
from src.runtime_helpers import Table, format_val
from src.error_handling import InterpolationParseError, ReturnSignal
from src.error_messaging import format_parse_error, error_message_unterminated_interpolation, error_message_included_file_not_found, error_message_generic
from lark import UnexpectedToken, UnexpectedInput, UnexpectedCharacters
from src.color_helpers import color_error, color_code

DISABLE_COLOR = not sys.stdout.isatty() or os.environ.get("NO_COLOR") == "1"

def say(val):
    print(val)

# All references to Enzo's 'number' atom are now 'number atom' or 'number_atom' in comments and user-facing messages.
def print_enzo_error(msg):
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
    print(f"{RED}{lines[0]}{RESET}")  # Print to stdout, not stderr
    # Remaining lines: treat as code block (if present)
    for code_line in lines[1:]:
        if code_line.strip():
            print(f"{BLACK_BG}{WHITE}{code_line.rstrip()}{RESET}")

def read_statement(stdin, interactive):
    buffer = []
    paren_depth = 0
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
        if line.strip().startswith('//=') and not buffer:
            # Pass test title through as a statement so it prints
            buffer.append(line)
            break
        if line.strip().startswith('//') and not buffer:
            continue

        # Update paren_depth for every '(' or ')' in the line
        for char in line:
            if char == '(':
                paren_depth += 1
            elif char == ')':
                paren_depth -= 1

        buffer.append(line)

        # Only break if we're not inside unclosed parens
        if paren_depth <= 0 and ';' in line:
            break

    return '\n'.join(buffer) if buffer else None

def run_enzo_file(filename):
    with open(filename) as f:
        lines = f.readlines()
    # Handle @include directives
    lines = list(process_includes(lines, base_dir=os.path.dirname(os.path.abspath(filename))))
    from io import StringIO
    fake_stdin = StringIO(''.join(lines))
    interactive = False
    while True:
        stmt = read_statement(fake_stdin, interactive)
        if stmt is None:
            break
        line = stmt.strip()
        if not line:
            continue
        # --- PRINT //= TITLES TO STDOUT, EVEN IN FILE MODE ---
        if line.startswith("//= "):
            print(line)
            continue
        # Skip full-line comments (but not //= titles)
        if line.startswith("//"):
            continue
        # Strip inline comments (for code lines only)
        if "//" in line:
            line = line.split("//", 1)[0].rstrip()
        if not line:
            continue
        try:
            result = eval_ast(parse(line), value_demand=True)
            # Only print if result is not None (including empty lists/tables)
            if result is not None:
                print(format_val(result))
        except InterpolationParseError:
            print_enzo_error(error_message_unterminated_interpolation())
        except (UnexpectedToken, UnexpectedInput, UnexpectedCharacters) as e:
            print_enzo_error(format_parse_error(e, src=line))
        except ReturnSignal as ret:
            print(format_val(ret.value))
        except Exception as e:
            # Print error message, code line, and caret underline for runtime errors
            print_enzo_error(error_message_generic(e))
            print(f"    {line}")
            print(f"    {'^' * len(line)}")

def process_includes(lines, base_dir=None, already_included=None):
    #Given a list of source lines, yield each line, but expand any `@include filename` directives inline.
    if already_included is None:
        already_included = set()
    if base_dir is None:
        base_dir = os.getcwd()

    for line in lines:
        striped = line.strip()
        if striped.startswith('@include '):
            _, fname = striped.split(None, 1)
            # Prevent duplicate includes in the same run
            abs_path = os.path.abspath(os.path.join(base_dir, fname))
            if abs_path in already_included:
                continue
            already_included.add(abs_path)
            if not os.path.isfile(abs_path):
                print(error_message_included_file_not_found(fname))
                continue
            with open(abs_path) as f:
                sub_lines = f.readlines()
            # Recursively process includes
            sub_base = os.path.dirname(abs_path)
            yield from process_includes(sub_lines, base_dir=sub_base, already_included=already_included)
        else:
            yield line

def main():
    # --- FILE RUNNER MODE ---
    if len(sys.argv) > 1:
        run_enzo_file(sys.argv[1])
        sys.exit(0)

    # --- REPL MODE ---
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
        # Print test titles (//= ...) to stdout as part of output
        if line.startswith("//="):
            print(line)
            continue
        # Skip full-line comments (but not //= titles)
        if line.startswith("//"):
            continue
        # Strip inline comments (for code lines only)
        if "//" in line:
            line = line.split("//", 1)[0].rstrip()
        if not line:
            continue

        try:
            ast = parse(line)
            result = eval_ast(ast, value_demand=True)
            # If result is a list (from Program), print each non-None value on its own line
            if isinstance(result, list):
                for val in result:
                    if val is not None:
                        if isinstance(val, (list, dict, Table)):
                            print(format_val(val))
                        else:
                            print(val)
            else:
                if result is not None:
                    if isinstance(result, (list, dict, Table)):
                        print(format_val(result))
                    else:
                        print(result)
        except InterpolationParseError:
            print(color_error(error_message_unterminated_interpolation()))
            print(color_code("    " + line))
            underline = "    " + " " * line.find("<") + "^"
            print(color_code(underline))
        except (UnexpectedToken, UnexpectedInput, UnexpectedCharacters) as e:
            # Use friendly error message for extra semicolon
            if isinstance(e, UnexpectedToken) and getattr(e, 'token', None):
                from src.error_messaging import error_message_unexpected_token
                msg = error_message_unexpected_token(e.token)
                print(color_error(msg))
                print(color_code("    " + line))
                underline = "    " + "^" * len(line)
                print(color_code(underline))
            else:
                fullmsg = format_parse_error(e, src=line)
                if "\n" in fullmsg:
                    errline, context = fullmsg.split("\n", 1)
                    print(color_error(errline))
                    print(color_code(context))
                else:
                    print(color_error(fullmsg))
        except ReturnSignal as ret:
            print(ret.value)
        except Exception as e:
            print(color_error(format_parse_error(e, src=line) if hasattr(e, 'line') else error_message_generic(str(e))))
            print(color_code("    " + line))
            print(color_code("    " + "^" * len(line)))
        # — CRITICAL FIX: after error or success, **continue the loop**
        # Don't break; keep processing all input!

if __name__ == "__main__":
    main()
