#!/usr/bin/env python3

import sys
sys.path.append('..')

from src.evaluator import eval_ast, _env, _initialize_builtin_variants
from src.enzo_parser.parser import parse

# Reset environment for clean testing but preserve built-ins
_env.clear()
_initialize_builtin_variants()

print("=== NAMELESS FUNCTION WITH STANDALONE EXPRESSION ===")
test_code1 = '''
($x: 1;
 $y: 2;
 $x + $y; // This should print 3
);
'''

print("Test code:")
print(test_code1)
print("Executing...")
ast = parse(test_code1)
result = eval_ast(ast)
print(f"Final result: {result}")

print("\n" + "="*50)

print("=== RECURSION TEST ===")
test_code2 = '''
$rec_n: 100;
rec_countdown: (
    param $rec_n: 3;
    $rec_n; // This should print each time
    If $rec_n is greater than 0, (
        $rec_n - 1 :> $rec_n;
        rec_countdown($rec_n);
    );
);

rec_countdown(1);
'''

print("Test code:")
print(test_code2)
print("Executing...")
_env.clear()
_initialize_builtin_variants()
ast = parse(test_code2)
result = eval_ast(ast)
print(f"Final result: {result}")
