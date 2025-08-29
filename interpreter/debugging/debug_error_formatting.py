#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env
from src.enzo_parser.parser import parse
from src.error_handling import EnzoRuntimeError
from src.error_messaging import format_parse_error

# Reset environment
_env.clear()

# Test the exact failing case
test_code = "$z-local; // error: undefined variable"

try:
    ast = parse(test_code)
    print("AST node code_line:", repr(ast[0].code_line))

    # This should raise an EnzoRuntimeError
    result = eval_ast(ast)
    print("Unexpected success:", result)

except EnzoRuntimeError as e:
    print("Caught EnzoRuntimeError:")
    print(f"  Message: {repr(str(e))}")
    print(f"  Has code_line: {hasattr(e, 'code_line')}")
    if hasattr(e, 'code_line'):
        print(f"  Error code_line: {repr(e.code_line)}")

    # Test how format_parse_error handles this
    formatted = format_parse_error(e, src=test_code)
    print("\nFormatted error:")
    print(repr(formatted))
    print("\nFormatted error (visual):")
    print(formatted)

except Exception as e:
    print(f"Other error: {e}")
    import traceback
    traceback.print_exc()
