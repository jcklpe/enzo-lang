#!/usr/bin/env python3

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from enzo_parser.parser import Parser
from enzo_parser.tokenizer import Tokenizer

def test_else_parsing():
    # Test the specific problematic syntax
    test_code = '''If $status-else, (
  "Won't print";),
Else, (
  "Fallback triggered";
);'''
    
    print(f"Testing: {test_code}")
    try:
        tokenizer = Tokenizer(test_code)
        tokens = tokenizer.tokenize()
        
        print("\nTokens:")
        for i, token in enumerate(tokens):
            if token.type not in ('WHITESPACE', 'COMMENT'):
                print(f"  {i}: {token}")
        
        parser = Parser(tokens, test_code)
        ast = parser.parse()
        print(f"✅ Parsed successfully")
        print(f"AST: {ast}")
    except Exception as e:
        print(f"❌ Parse error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_else_parsing()
