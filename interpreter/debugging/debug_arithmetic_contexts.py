#!/usr/bin/env python3

# Debug arithmetic contexts to understand where bare expressions are allowed

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.enzo_parser.parser import Parser
from src.evaluator import eval_ast
from src.enzo_parser.ast_nodes import Program

# Test various arithmetic contexts to see where bare expressions are allowed
test_cases = [
    # Rebinding contexts
    ('$x1: 5; $x1 + 1 :> $x1; $x1;', 'Rebinding with :>'),
    ('$x2: 5; $x2 <: $x2 + 1; $x2;', 'Rebinding with <:'),

    # Assignment contexts
    ('$x3: 5; $y3: 3; $result3: $x3 + $y3; $result3;', 'Assignment with :'),

    # Top-level expressions
    ('5 + 3;', 'Top-level expression'),

    # Function atom contexts
    ('($x4: 5; $y4: 3; $x4 + $y4);', 'Function atom expression'),

    # String interpolation
    ('$x5: 5; "Result: <$x5 + 1>";', 'String interpolation'),

    # Comparison contexts
    ('$x6: 5; If $x6 + 1 is 6, "yes"; end;', 'Comparison context'),

    # List contexts
    ('$x7: 1; $y7: 2; [$x7 + 1, $y7 + 2];', 'List context'),

    # Pipeline contexts
    ('$x8: 5; $x8 then ($this + 1);', 'Pipeline context'),

    # Direct arithmetic without variables
    ('10 + 5;', 'Direct arithmetic'),

    # Nested arithmetic
    ('$x9: 2; $y9: 3; $x9 + $y9 * 2;', 'Nested arithmetic'),
]

print("=== TESTING ARITHMETIC IN DIFFERENT CONTEXTS ===")

for i, (code, description) in enumerate(test_cases, 1):
    print(f"\nTest {i}: {description}")
    print(f"Code: {code}")
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
