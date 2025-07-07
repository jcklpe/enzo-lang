#!/usr/bin/env python3

import sys
import os

# Add the interpreter directory to the path so we can import src modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.enzo_parser.tokenizer import Tokenizer

code = "$simple: (param $x: ; $x);"
print(f"Tokenizing: {code}")
tokens = Tokenizer(code).tokenize()
for i, token in enumerate(tokens):
    print(f"{i}: {token}")
