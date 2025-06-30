#!/usr/bin/env python3

import sys
sys.path.append('src')

from enzo_parser.tokenizer import Tokenizer

# Test the failing case
code = """($z: 101;
$t: 102;
return(($z + $t));
)"""

tokenizer = Tokenizer(code)
tokens = tokenizer.tokenize()
for i, token in enumerate(tokens):
    print(f'{i:2d}: {token}')
