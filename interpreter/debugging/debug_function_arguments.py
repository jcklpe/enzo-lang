#!/usr/bin/env python3

# Debug function arguments to see if they are demand-driven contexts

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.enzo_parser.parser import Parser
from src.evaluator import eval_ast
from src.enzo_parser.ast_nodes import Program

# Test function argument contexts with detailed output
test_cases = [
    # Test 1: What actually gets passed to function parameters?
    '''
    test-func: (
        param $arg1: ;
        param $arg2: ;
        return([$arg1, $arg2]);
    );
    test-func((2 + 2), (3 + 3));
    ''',

    # Test 2: Can we call the received arguments as functions?
    '''
    test-func2: (
        param $arg1: ;
        param $arg2: ;
        $result1: $arg1();
        $result2: $arg2();
        return([$result1, $result2]);
    );
    $stored1: (2 + 2);
    $stored2: (3 + 3);
    test-func2($stored1, $stored2);
    ''',

    # Test 3: Mixed direct values and function atoms
    '''
    test-func3: (
        param $direct: ;
        param $computed: ;
        param $stored: ;
        return([$direct, $computed, $stored]);
    );
    $stored-func: (10 + 5);
    test-func3(42, (7 * 6), $stored-func);
    ''',

    # Test 4: Can we invoke stored functions that were passed as args?
    '''
    test-func4: (
        param $stored: ;
        $invoked: $stored();
        return($invoked);
    );
    $my-func: (100 + 200);
    test-func4($my-func);
    '''
]

print("=== TESTING FUNCTION ARGUMENT CONTEXTS ===")

for i, code in enumerate(test_cases, 1):
    print(f"\nTest {i}: Function arguments")
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
        import traceback
        traceback.print_exc()
