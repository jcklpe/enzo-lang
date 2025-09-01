#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing but preserve built-ins
_env.clear()
_initialize_builtin_variants()

test_code = """
clos_make_counter: (
    $count: 0; // This variable is private to the closure's environment.
    return( @(
        $count + 1 :> $count; // Mutate the captured variable
        return($count);
    ) );
);

$clos_counter_A: clos_make_counter();
"""

test_calls = [
    "$clos_counter_A();",
    "$clos_counter_A();",
    "$clos_counter_B: clos_make_counter();",
    "$clos_counter_B();",
    "$clos_counter_A();"
]

print("Parsing initial setup...")
ast = parse(test_code)
print("Executing initial setup...")
results = eval_ast(ast)

print(f"Setup Results: {results}")

# Now execute each call individually
for i, call_code in enumerate(test_calls):
    print(f"\n--- Call {i+1}: {call_code.strip()} ---")
    call_ast = parse(call_code)
    call_result = eval_ast(call_ast)
    print(f"Result: {call_result}")

    # Check the counter state after each call
    if 'clos_counter_A' in _env:
        counter_a = _env['clos_counter_A']
        if hasattr(counter_a, 'closure_env') and 'count' in counter_a.closure_env:
            print(f"Counter A count after call: {counter_a.closure_env['count']}")

    if 'clos_counter_B' in _env:
        counter_b = _env['clos_counter_B']
        if hasattr(counter_b, 'closure_env') and 'count' in counter_b.closure_env:
            print(f"Counter B count after call: {counter_b.closure_env['count']}")

# Let's also inspect the closure environments
print(f"\nEnvironment keys: {list(_env.keys())}")

if 'clos_counter_A' in _env:
    counter_a = _env['clos_counter_A']
    print(f"Counter A type: {type(counter_a)}")
    if hasattr(counter_a, 'closure_env'):
        print(f"Counter A closure env: {counter_a.closure_env}")
        print(f"Counter A closure env type: {type(counter_a.closure_env)}")
        if 'count' in counter_a.closure_env:
            print(f"Counter A count value: {counter_a.closure_env['count']}")

if 'clos_counter_B' in _env:
    counter_b = _env['clos_counter_B']
    print(f"Counter B type: {type(counter_b)}")
    if hasattr(counter_b, 'closure_env'):
        print(f"Counter B closure env: {counter_b.closure_env}")
        print(f"Counter B closure env type: {type(counter_b.closure_env)}")
        if 'count' in counter_b.closure_env:
            print(f"Counter B count value: {counter_b.closure_env['count']}")
