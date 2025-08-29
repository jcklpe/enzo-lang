#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env
from src.enzo_parser.parser import parse
from src.error_handling import EnzoRuntimeError

# Test the exact SCOPE LEAKAGE case
_env.clear()

scope_leakage_test = """
If True, (
    $z-local: "local-to-if";
);
$z-local; // error: undefined variable
"""

print("=== SCOPE LEAKAGE Test ===")
try:
    ast = parse(scope_leakage_test)
    print(f"AST length: {len(ast)}")

    for i, node in enumerate(ast):
        print(f"Node {i}: {type(node)}")
        if hasattr(node, 'code_line'):
            print(f"  code_line: {repr(node.code_line)}")

    print("\nEvaluating...")
    result = eval_ast(ast)
    print("Unexpected success")

except EnzoRuntimeError as e:
    print(f"EnzoRuntimeError: {e}")
    print(f"Error code_line: {repr(getattr(e, 'code_line', 'NO CODE_LINE'))}")

# Now test the exact SCOPE ISOLATION case
_env.clear()

scope_isolation_test = """
$scope-test: "global";
If False, (
    $if-var: 1;
), Else, (
    $scope-test: "else-branch";
    "In Else: <$scope-test>";
    $if-var; // error: undefined variable (was defined in a separate scope)
);
"""

print("\n=== SCOPE ISOLATION Test ===")
try:
    ast = parse(scope_isolation_test)
    print(f"AST length: {len(ast)}")

    print("\nEvaluating...")
    result = eval_ast(ast)
    print("Unexpected success")

except EnzoRuntimeError as e:
    print(f"EnzoRuntimeError: {e}")
    print(f"Error code_line: {repr(getattr(e, 'code_line', 'NO CODE_LINE'))}")
