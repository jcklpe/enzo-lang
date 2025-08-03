#!/usr/bin/env python3

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from enzo_parser.parser import parse
from evaluator import eval_ast

def debug_sequential_parsing():
    with open('tests/test-modules/subset-conditional-flow.enzo', 'r') as f:
        content = f.read()
    
    print("=== DEBUGGING SEQUENTIAL PARSING ===")
    
    try:
        # Parse the entire file first
        statements = parse(content)
        
        print(f"✅ Parsing successful. Found {len(statements)} statements")
        
        # Now try evaluating statement by statement
        for i, stmt in enumerate(statements):
            print(f"\n--- Statement {i+1}: {type(stmt).__name__} ---")
            try:
                # Evaluate the statement directly
                result = eval_ast(stmt)
                if result is not None and result != "":
                    print(f"Result: {result}")
            except Exception as e:
                print(f"❌ Evaluation error on statement {i+1}: {e}")
                print(f"Statement: {stmt}")
                import traceback
                traceback.print_exc()
                break
        
    except Exception as e:
        print(f"❌ Parse error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_sequential_parsing()
