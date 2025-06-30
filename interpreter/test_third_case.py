#!/usr/bin/env python3

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from enzo_parser.tokenizer import Tokenizer
from enzo_parser.parser import Parser

def test_third_case():
    # Test the third case specifically - note the semicolon after return
    code = """($z: 101;
$t: 102;
return(($z + $t));
);"""

    print('Testing third case:')
    print(repr(code))
    print()
    print('Code:')
    print(code)
    print()

    # Tokenize
    tokenizer = Tokenizer(code)
    tokens = tokenizer.tokenize()
    print('Tokens:')
    for i, token in enumerate(tokens):
        print(f'{i:2d}: {token}')
    print()

    # Parse
    parser = Parser(tokens, code)
    try:
        result = parser.parse()
        print('Parse successful!')
        print(f'Result: {result}')
        print(f'Result type: {type(result)}')
    except Exception as e:
        print(f'Parse failed: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_third_case()
