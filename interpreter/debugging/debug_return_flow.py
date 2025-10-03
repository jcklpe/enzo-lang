#!/usr/bin// Test simple # Test simple return behavior first
simple_test = """
rec_factorial: (
    param $n: ;
    If ($n is 1) {
        print("Base case reached with n =", $n)
        return(1)
    }
    print("Should not reach here if return works")
    return(999)
)

print("Testing with n=1 (should return immediately):")
$result: rec_factorial(1)
print("Result:", $result)
""" first
simple_test = """
rec_factorial :: ($n) -> {
    If ($n is 1) {
        print("Base case reached with n =", $n)
        return(1)
    }
    print("Should not reach here if return works")
    return(999)
}

print("Testing with n=1 (should return immediately):")
$result :: rec_factorial(1)
print("Result:", $result)
"""

import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing
_env.clear()
_initialize_builtin_variants()

# Test simple return behavior first
simple_test = """
rec_factorial :: ($n) -> {
    If ($n is 1) {
        print("Base case reached with n =", $n)
        return(1)
    }
    print("Should not reach here if return works")
    return(999)
}

print("Testing with n=1 (should return immediately):")
$result: rec_factorial(1)
print("Result:", $result)
"""

print("=== SIMPLE RETURN TEST ===")
try:
    ast = parse(simple_test)
    result = eval_ast(ast)
    print("Simple test completed successfully")
except Exception as e:
    print(f"Error in simple test: {e}")
    import traceback
    traceback.print_exc()