#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing but keep built-ins
_env.clear()
_initialize_builtin_variants()

# Test 1: Direct rebinding in while loop (this works)
test1 = '''$test: True;
$counter: 0;
Loop while $test and $counter is less than 2, (
    $counter + 1 :> $counter;
    "Counter: <$counter>";
    If $counter is 2, (
        False :> $test;
        "Set test to False";
    );
);
"Final test: <$test>";
$test;
'''

print("=== Test 1: Conditional rebinding in while loop ===")
ast1 = parse(test1)
result1 = eval_ast(ast1)
print(f"Result: {result1} (should be False)")

# Test 2: Same logic but step by step to see where it breaks
print("\n=== Test 2: Simpler step by step ===")
_env.clear()
_initialize_builtin_variants()

# Setup
eval_ast(parse('$test: True;'))
print(f"Initial test: {eval_ast(parse('$test;'))}")

# Test direct rebinding in conditional
eval_ast(parse('''If True, (
    False :> $test;
);'''))
print(f"After conditional rebinding: {eval_ast(parse('$test;'))}")

# Reset and test in loop context
_env.clear()
_initialize_builtin_variants()
eval_ast(parse('$test: True;'))

# Create a loop environment manually to see what happens
from src.evaluator import eval_ast
print(f"\nBefore loop setup: {eval_ast(parse('$test;'))}")

# Test the exact loop structure
result = eval_ast(parse('''$test: True;
Loop while $test, (
    If True, (
        False :> $test;
        "Should set test to False";
    );
);
$test;'''))
print(f"After manual loop: {result}")# Test 3: Direct rebinding outside any control flow
print("\n=== Test 3: Direct rebinding (control) ===")
_env.clear()
_initialize_builtin_variants()

test3 = '''$direct: True;
False :> $direct;
$direct;
'''
result3 = eval_ast(parse(test3))
print(f"Direct rebinding result: {result3} (should be False)")

# Test 4: Rebinding in conditional only
print("\n=== Test 4: Rebinding in conditional only ===")
_env.clear()
_initialize_builtin_variants()

test4 = '''$cond: True;
If True, (
    False :> $cond;
);
$cond;
'''
result4 = eval_ast(parse(test4))
print(f"Conditional rebinding result: {result4} (should be False)")
