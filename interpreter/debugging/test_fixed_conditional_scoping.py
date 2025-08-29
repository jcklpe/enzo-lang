#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env
from src.enzo_parser.parser import parse

# Reset environment for clean testing
_env.clear()

print("=== Testing Fixed Conditional Scoping ===")

# Test 1: Basic shadowing
print("\n1. Basic shadowing test:")
test1 = """
$cond-shadow-global: "global";
If True, (
    $cond-shadow-global: "if-shadow";
    "Inside If: <$cond-shadow-global>";
);
"Outside If: <$cond-shadow-global>";
"""

try:
    ast1 = parse(test1)
    result1 = eval_ast(ast1)
    print("SUCCESS: Basic shadowing works!")
    print("Results should be: 'Inside If: if-shadow' and 'Outside If: global'")
except Exception as e:
    print("ERROR:", e)
    import traceback
    traceback.print_exc()

# Reset environment
_env.clear()

# Test 2: Scope leakage prevention
print("\n2. Scope leakage test:")
test2 = """
If True, (
    $z-local: "local-to-if";
    "Local variable value: <$z-local>";
);
$z-local;
"""

try:
    ast2 = parse(test2)
    result2 = eval_ast(ast2)
    print("UNEXPECTED SUCCESS - should have errored on undefined variable")
except Exception as e:
    if "undefined variable" in str(e):
        print("SUCCESS: Scope leakage properly prevented")
    else:
        print("WRONG ERROR:", e)

# Reset environment
_env.clear()

# Test 3: Else block isolation
print("\n3. Else block isolation test:")
test3 = """
$scope-test: "global";
If False, (
    $if-var: 1;
), Else, (
    $scope-test: "else-branch";
    "In Else: <$scope-test>";
    $if-var;
);
"""

try:
    ast3 = parse(test3)
    result3 = eval_ast(ast3)
    print("UNEXPECTED SUCCESS - should have errored on undefined $if-var")
except Exception as e:
    if "undefined variable" in str(e):
        print("SUCCESS: Else block properly isolated from If block")
    else:
        print("WRONG ERROR:", e)
