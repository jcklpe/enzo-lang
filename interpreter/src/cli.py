import os
import sys

# Add the interpreter directory to the path so we can import src modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.runtime_helpers import clear_debug_log
clear_debug_log()  # <-- Clear the debug log at the very start

import re
from src.enzo_parser.parser import parse  # Use new parser
from src.evaluator    import eval_ast
from src.runtime_helpers import Table, format_val, log_debug

# CRITICAL INFO: ALL ERROR HANDLING MUST BE USE THE CENTRALIZED error_handling.py MODULE
from src.error_handling import InterpolationParseError, ReturnSignal, EnzoParseError, EnzoRuntimeError

# CRITICAL INFO: ALL ERROR MESSAGING MUST BE USE THE CENTRALIZED error_messaging.py MODULE
from src.error_messaging import format_parse_error, error_message_unterminated_interpolation, error_message_included_file_not_found, error_message_generic
from src.color_helpers import color_error, color_code



DISABLE_COLOR = not sys.stdout.isatty() or os.environ.get("NO_COLOR") == "1"

def say(val):
    print(val)

# All references to Enzo's 'number' atom are now 'number atom' or 'number_atom' in comments and user-facing messages.
def print_enzo_error(msg, color="red"):
    """Print error message with proper color formatting"""

    lines = msg.split('\n')

    # First line (error description) in red
    if lines:
        print(color_error(lines[0]))

        # Remaining lines (code context) with black background
        for i, line in enumerate(lines[1:]):
            print(color_code(line.rstrip()))

def read_statement(stdin, interactive):
    buffer = []
    paren_depth = 0
    brace_depth = 0
    bracket_depth = 0
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
            buffer.append(line)
            break
        if line.strip().startswith('//') and not buffer:
            continue

        # Update paren_depth, brace_depth, bracket_depth for every '(', ')', '{', '}', '[', ']'
        for char in line:
            if char == '(':
                paren_depth += 1
            elif char == ')':
                paren_depth -= 1
            elif char == '{':
                brace_depth += 1
            elif char == '}':
                brace_depth -= 1
            elif char == '[':
                bracket_depth += 1
            elif char == ']':
                bracket_depth -= 1

        buffer.append(line)

        # Only break if all depths are zero and ';' is in the line
        if paren_depth <= 0 and brace_depth <= 0 and bracket_depth <= 0 and ';' in line:
            break

    return '\n'.join(buffer) if buffer else None

def split_statements(lines):
    # Split a list of lines into complete statements (respecting nesting)
    stmts = []
    buffer = []
    paren_depth = 0
    brace_depth = 0
    bracket_depth = 0
    if_depth = 0  # Track control flow depth
    block_comment_depth = 0  # Track block comment depth

    for line in lines:
        stripped = line.rstrip('\n')
        # Skip blank/comment lines unless already in a statement
        if not stripped and not buffer:
            continue
        # IMPORTANT: Test section delimiters force statement breaks
        if stripped.strip().startswith('//='):
            if buffer:  # If we have a pending statement, close it first
                stmts.append(buffer)
                buffer = []
                # Reset all depth counters for new test section
                paren_depth = 0
                brace_depth = 0
                bracket_depth = 0
                if_depth = 0
                block_comment_depth = 0
            stmts.append([stripped])
            continue
        if stripped.strip().startswith('//') and not buffer:
            continue

        # First, scan for block comments to determine what part of the line to parse for depths
        # We need to track block comment state to know what parts are "real code"
        line_to_parse = ""
        i = 0
        line_block_depth = block_comment_depth
        while i < len(stripped):
            if line_block_depth > 0:
                # We're inside a block comment, look for closing '/
                if i < len(stripped) - 1 and stripped[i:i+2] == "'/":
                    line_block_depth -= 1
                    i += 2
                else:
                    i += 1
            else:
                # We're outside block comments, look for opening /` or regular code
                if i < len(stripped) - 1 and stripped[i:i+2] == "/'":
                    line_block_depth += 1
                    i += 2
                elif stripped[i:i+2] == "//":
                    # Regular comment - ignore rest of line
                    break
                else:
                    # Regular code - add to line_to_parse
                    line_to_parse += stripped[i]
                    i += 1

        # Update global block comment depth
        block_comment_depth = line_block_depth

        # Track control flow keywords (only in non-comment parts)
        import re
        # Check for If/For/While keywords (must be whole words)
        if re.search(r'\b(If|For|While)\b', line_to_parse):
            if_depth += 1
        # In new syntax, closing parenthesis followed by semicolon ends control flow
        if re.search(r'\);\s*$', line_to_parse) and if_depth > 0:
            if_depth = max(0, if_depth - 1)  # Prevent negative depth
        # Keep old 'end' keyword support for backwards compatibility
        if re.search(r'\bend\b', line_to_parse):
            if_depth = max(0, if_depth - 1)  # Prevent negative depth

        # Track parentheses/brackets/braces (only in non-comment parts)
        for char in line_to_parse:
            if char == '(':
                paren_depth += 1
            elif char == ')':
                paren_depth -= 1
            elif char == '{':
                brace_depth += 1
            elif char == '}':
                brace_depth -= 1
            elif char == '[':
                bracket_depth += 1
            elif char == ']':
                bracket_depth -= 1

        buffer.append(stripped)
        # Only break on semicolon if all depths are zero and semicolon is not in a comment
        has_semicolon = ';' in line_to_parse  # Only check semicolons outside of comments and block comments
        if (paren_depth <= 0 and brace_depth <= 0 and bracket_depth <= 0 and
            if_depth <= 0 and block_comment_depth <= 0 and has_semicolon):
            stmts.append(buffer)
            buffer = []
    if buffer:
        stmts.append(buffer)
    return stmts

def run_enzo_file(filename):
    with open(filename) as f:
        lines = f.readlines()
    lines = list(process_includes(lines, base_dir=os.path.dirname(os.path.abspath(filename))))
    stmts = split_statements(lines)
    for stmt_lines in stmts:
        statement = '\n'.join(stmt_lines).strip()
        if not statement:
            continue
        if statement.strip().startswith('//='):
            print(statement.rstrip())
            continue
        # --- NEW: If this block is a list of single-line statements, process each line independently ---
        # BUT: Don't do this if the block starts with '(' (function atom) or other multi-line constructs
        # ALSO: Don't do this if any line contains 'then (' (pipeline with function atom)
        # ALSO: Don't do this if the block contains control flow keywords (If, Else, end)
        if (all(';' in line for line in stmt_lines) and len(stmt_lines) > 1 and
            not any(line.strip().startswith(('(', '[', '{')) for line in stmt_lines) and
            not any('then (' in line for line in stmt_lines) and
            not any(any(keyword in line for keyword in ['If ', 'For ', 'While ', 'Else', 'end;', 'end']) for line in stmt_lines)):
            for line in stmt_lines:
                line = line.strip()
                if not line:
                    continue
                # Strip inline comments (for code lines only)
                if '//' in line:
                    line = line.split('//', 1)[0].rstrip()
                if not line:
                    continue
                try:
                    result = eval_ast(parse(line), value_demand=True)
                    # Don't print None values
                    if result is not None:
                        print(format_val(result))
                except InterpolationParseError as e:
                    msg = format_parse_error(e, src=line)
                    if "\n" in msg:
                        errline, context = msg.split("\n", 1)
                        print_enzo_error(errline + "\n" + context)
                    else:
                        print_enzo_error(msg)
                    continue
                except EnzoParseError as e:
                    msg = format_parse_error(e, src=line)
                    if "\n" in msg:
                        errline, context = msg.split("\n", 1)
                        print_enzo_error(errline + "\n" + context)
                    else:
                        print_enzo_error(msg)
                    continue
                except EnzoParseError as e:
                    msg = format_parse_error(e, src=line)
                    print_enzo_error(msg)
                    continue
                except EnzoRuntimeError as e:
                    msg = format_parse_error(e, src=line)
                    print_enzo_error(msg)
                    continue
                except Exception as e:
                    msg = format_parse_error(e, src=line) if hasattr(e, 'code_line') or hasattr(e, 'line') or hasattr(e, 'column') else error_message_generic(str(e))
                    print_enzo_error(msg)
                    continue
            continue  # move to next block after processing all lines
        # Strip inline comments only for single-line statements
        # Multi-line statements (like function atoms) should not have comments stripped
        # since the tokenizer handles them properly
        is_multiline = '\n' in statement
        original_statement = statement  # Keep original for error reporting
        if not is_multiline and '//' in statement:
            statement = statement.split('//', 1)[0].rstrip()
        if not statement:
            continue

        # DEBUG: Log what we're about to parse
        log_debug(f"[CLI] About to parse statement: {repr(statement)}")

        try:
            # Use parse_program for multi-line statements, parse for single statements
            if '\n' in statement or ';' in statement.rstrip(';'):
                # Multi-line or multiple statements - use program parser
                from src.enzo_parser.parser import parse_program
                program = parse_program(statement)

                # Evaluate statements one by one to handle errors gracefully
                if hasattr(program, 'statements'):
                    for stmt in program.statements:
                        result = eval_ast(stmt, value_demand=True)
                        # Don't print None values
                        if result is not None:
                            # If the result is itself a list from a loop, print each element
                            if isinstance(result, list):
                                for sub_item in result:
                                    if sub_item is not None:
                                        print(format_val(sub_item))
                            else:
                                print(format_val(result))
                else:
                    # Fallback for non-program results
                    result = eval_ast(program, value_demand=True)
                    # Don't print None values
                    if result is not None:
                        print(format_val(result))
            else:
                # Single statement - use regular parser
                result = eval_ast(parse(statement), value_demand=True)
                # Don't print None values
                if result is not None:
                    print(format_val(result))
        except InterpolationParseError as e:
            msg = format_parse_error(e, src=original_statement)
            if "\n" in msg:
                errline, context = msg.split("\n", 1)
                print_enzo_error(errline + "\n" + context)
            else:
                print_enzo_error(msg)
            continue
        except EnzoParseError as e:
            msg = format_parse_error(e, src=original_statement)
            if "\n" in msg:
                errline, context = msg.split("\n", 1)
                print_enzo_error(errline + "\n" + context)
            else:
                print_enzo_error(msg)
            continue
        except EnzoParseError as e:
            msg = format_parse_error(e, src=original_statement)
            print_enzo_error(msg)
            continue
        except EnzoRuntimeError as e:
            msg = format_parse_error(e, src=original_statement)
            print_enzo_error(msg)
            continue
        except Exception as e:
            msg = format_parse_error(e, src=original_statement) if hasattr(e, 'code_line') or hasattr(e, 'line') or hasattr(e, 'column') else error_message_generic(str(e))
            print_enzo_error(msg)
            continue

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
                    # Don't print None values
                    if val is not None:
                        if isinstance(val, (list, dict, Table)):
                            print(format_val(val))
                        else:
                            print(val)
            else:
                # Don't print None values
                if result is not None:
                    if isinstance(result, (list, dict, Table)):
                        print(format_val(result))
                    else:
                        print(result)
        except InterpolationParseError:
            print(color_error(error_message_unterminated_interpolation()))
            print(color_code("    " + line))
        except EnzoParseError as e:
            msg = format_parse_error(e, src=line)
            if "\n" in msg:
                errline, context = msg.split("\n", 1)
                print(color_error(errline))
                print(color_code(context))
            else:
                print(color_error(msg))
        except EnzoParseError as e:
            msg = format_parse_error(e, src=line)
            if "\n" in msg:
                errline, context = msg.split("\n", 1)
                print(color_error(errline))
                print(color_code(context))
            else:
                print(color_error(msg))
        except EnzoRuntimeError as e:
            msg = format_parse_error(e, src=line)
            if "\n" in msg:
                errline, context = msg.split("\n", 1)
                print(color_error(errline))
                print(color_code(context))
            else:
                print(color_error(msg))
        except ReturnSignal as ret:
            print(ret.value)
        except Exception as e:
            # Use centralized error messaging for all errors (including runtime/type errors)
            msg = format_parse_error(e, src=line) if hasattr(e, 'code_line') or hasattr(e, 'line') or hasattr(e, 'column') else error_message_generic(str(e))
            print(color_error(msg))
            print(color_code("    " + line))
        # — CRITICAL FIX: after error or success, **continue the loop**
        # Don't break; keep processing all input!

if __name__ == "__main__":
    main()
