#!/usr/bin/env python3

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from enzo_parser.tokenizer import Tokenizer
from enzo_parser.parser import Parser

def debug_third_case():
    # The exact third test case from isolated.debug.enzo
    code = """($z: 101;
$t: 102;
return(($z + $t));
);"""

    print('Third test case code:')
    print(repr(code))
    print()
    print('Code:')
    print(code)
    print()

    # Tokenize
    tokenizer = Tokenizer(code)
    tokens = tokenizer.tokenize()

    print(f'Total tokens: {len(tokens)}')
    print('Tokens:')
    for i, token in enumerate(tokens):
        print(f'{i:2d}: {token}')
    print()

    # Parse
    parser = Parser(code)
    try:
        result = parser.parse()
        print('Parse successful!')
        print(f'Result: {result}')
    except Exception as e:
        print(f'Parse failed: {e}')
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_third_case()
