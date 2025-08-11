#!/usr/bin/env python3

# Detailed debugging for control flow parsing

from src.enzo_parser.tokenizer import Tokenizer
from src.enzo_parser.parser import Parser
from src.evaluator import eval_ast

def test_control_flow():
    # Test the exact failing case from the test file
    code = '''$status-if: "ready";

If $status-if,
  "Ready!"; // should print "Ready!"
end;'''

    print("=== TESTING CONTROL FLOW DETAILED ===")
    print(f"Code:\n{code}")

    # Test tokenization
    print("\n=== TOKENIZATION ===")
    tokenizer = Tokenizer(code)
    tokens = tokenizer.tokenize()
    for i, token in enumerate(tokens):
        if token.type not in ['WHITESPACE', 'NEWLINE']:
            print(f"{i}: {token}")

    # Test parsing
    print("\n=== PARSING ===")
    try:
        parser = Parser(code)
        ast = parser.parse()
        print(f"SUCCESS: {ast}")
    except Exception as e:
        print(f"PARSE ERROR: {e}")
        import traceback
        traceback.print_exc()
        return

    # Test evaluation
    print("\n=== EVALUATION ===")
    try:
        # Set up environment (no need to set $status-if since it's defined in code)
        env = {}
        for stmt in ast:
            result = eval_ast(stmt, env=env)
            if result is not None:
                print(f"Statement result: {result}")
    except Exception as e:
        print(f"EVAL ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_control_flow()
