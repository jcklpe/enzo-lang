import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Clear and reinitialize environment
_env.clear()
_initialize_builtin_variants()

# Simplified test to isolate the issue
test_code = '''
$test-var: True;
Loop, (
    "Direct loop body rebind";
    False :> $test-var;
    $test-var;
    end-loop;
);
$test-var;
'''

print("=== Test 1: Direct rebind in loop body ===")
ast = parse(test_code)
statements = ast if isinstance(ast, list) else ast.statements

for statement in statements:
    result = eval_ast(statement)

print(f"Final $test-var: {_env.get('$test-var', 'NOT_FOUND')}")

# Reset for second test
_env.clear()
_initialize_builtin_variants()

# Test with rebind inside If statement
test_code2 = '''
$test-var: True;
Loop, (
    "Loop body with If statement";
    If True, (
        "Inside If statement";
        False :> $test-var;
    );
    $test-var;
    end-loop;
);
$test-var;
'''

print("\n=== Test 2: Rebind inside If statement in loop ===")
ast2 = parse(test_code2)
statements2 = ast2 if isinstance(ast2, list) else ast2.statements

for statement in statements2:
    result = eval_ast(statement)

print(f"Final $test-var: {_env.get('$test-var', 'NOT_FOUND')}")