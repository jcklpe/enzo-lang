#!/usr/bin/env python3

# Debug what happens when we try to invoke function arguments

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.enzo_parser.parser import Parser
from src.evaluator import eval_ast
from src.enzo_parser.ast_nodes import Program

# Simple test cases
test_cases = [
    # Test 1: Can we invoke a stored function?
    '''
    $my-func: (10 + 20);
    $result: $my-func();
    $result;
    ''',

    # Test 2: What type is a function argument?
    '''
    test-func: (
        param $arg: ;
        return($arg);
    );
    $stored: (5 + 5);
    test-func($stored);
    ''',

    # Test 3: What happens when we try to invoke an argument that's a value?
    '''
    test-func2: (
        param $arg: ;
        $invoked: $arg();
        return($invoked);
    );
    test-func2(42);
    ''',
]

print("=== TESTING ARGUMENT INVOCATION ===")

for i, code in enumerate(test_cases, 1):
    print(f"\nTest {i}: Argument invocation")
    print(f"Code: {code.strip()}")
    try:
        parser = Parser(code)
        ast = parser.parse()
        print(f"✅ Parsed successfully")

        # Convert to Program if it's a list
        if isinstance(ast, list):
            ast = Program(ast)

        result = eval_ast(ast, value_demand=True)
        print(f"Result: {result}")

    except Exception as e:
        print(f"❌ Error: {e}")
