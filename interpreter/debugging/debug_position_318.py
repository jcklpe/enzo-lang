#!/usr/bin/env python3

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def check_position():
    with open('tests/test-modules/subset-conditional-flow.enzo', 'r') as f:
        content = f.read()
    
    print(f"Content length: {len(content)}")
    print(f"Character at position 318: '{content[318] if len(content) > 318 else 'EOF'}'")
    print(f"Context around position 318:")
    start = max(0, 318 - 50)
    end = min(len(content), 318 + 50)
    print(f"'{content[start:end]}'")
    print(f"Positions: {start}-{end}")
    
    # Let's also check what tokens are around that position
    from enzo_parser.tokenizer import Tokenizer
    tokenizer = Tokenizer(content)
    tokens = tokenizer.tokenize()
    
    print("\nTokens around position 318:")
    for token in tokens:
        if 310 <= token.start <= 330:
            print(f"  {token}")

if __name__ == "__main__":
    check_position()
