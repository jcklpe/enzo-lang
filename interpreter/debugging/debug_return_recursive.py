#!/usr/bin/env python3
import sys
sys.path.append('..')
from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing
_env.clear()
_initialize_builtin_variants()

# Test what happens with recursive calls
recursive_test = """
rec_factorial: (
    param $n: ;
    "Called with n = <$n>";
    If $n is at most 1, (
        "Base case reached! n = <$n>";
        return(1);
    );
    "Recursive case for n = <$n>";
    $result: $n * rec_factorial($n - 1);
    "Got result <$result> for n = <$n>";
    return($result);
);

"=== Testing factorial(2) ===";
$test_result: rec_factorial(2);
"Final result: <$test_result>";
"""

print("=== RECURSIVE TEST ===")
try:
    ast = parse(recursive_test)
    result = eval_ast(ast)
    print("Recursive test completed successfully")
except Exception as e:
    print(f"Error in recursive test: {e}")
    import traceback
    traceback.print_exc()