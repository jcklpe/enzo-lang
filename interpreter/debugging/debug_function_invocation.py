#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing but preserve built-ins
_env.clear()
_initialize_builtin_variants()

# Test the problematic function invocation with both function styles
test_code = '''
$function1: (
    param $a: 4;
    $x: 5;
    return($x + $a);
);
$function1;      // returns 9
function1();     // returns 9
$function1();    // returns 9
$function1(5);   // returns 10

function2: ($y: 2; $y + 3);
$function2;      // returns 9
function2();     // returns 9
$function2();    // returns 9
$function2(5);   // returns 10
'''

print("=== Parsing and evaluating function invocation test ===")
try:
    statements = parse(test_code)
    print(f"Parse successful. AST: {statements}")

    # Print details of each statement
    for i, stmt in enumerate(statements):
        print(f"\nStatement {i}: {type(stmt).__name__}")
        print(f"  AST: {stmt}")
        try:
            result = eval_ast(stmt)
            print(f"  Result: {result}")
        except Exception as e:
            print(f"  Error: {e}")

except Exception as e:
    print(f"Error during parsing: {e}")