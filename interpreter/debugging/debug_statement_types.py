#!/usr/bin/env python3

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from enzo_parser.parser import parse

def debug_statement_types():
    with open('tests/test-modules/subset-conditional-flow.enzo', 'r') as f:
        content = f.read()
    
    print("=== STATEMENT TYPES ===")
    
    try:
        statements = parse(content)
        
        for i, stmt in enumerate(statements):
            print(f"Statement {i+1}: {type(stmt).__name__} - {stmt}")
        
    except Exception as e:
        print(f"❌ Parse error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_statement_types()
