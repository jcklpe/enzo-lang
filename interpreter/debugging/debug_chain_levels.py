# Debug each level of the parsing chain
import sys
sys.path.insert(0, 'src')

from src.enzo_parser.parser import Parser

code = 'If $status, ("Ready!";);'

print("Testing each level of the parsing chain")

try:
    parser = Parser(code)
    parser.advance()  # consume 'If'

    print("Current token:", parser.peek())

    print("\n=== Testing parse_logical_expression ===")
    result = parser.parse_logical_expression()
    print("Result:", result, type(result))

    # Reset and test the next level
    parser2 = Parser(code)
    parser2.advance()  # consume 'If'

    print("\n=== Testing parse_not_expression ===")
    result2 = parser2.parse_not_expression()
    print("Result:", result2, type(result2))

    # Reset and test the next level
    parser3 = Parser(code)
    parser3.advance()  # consume 'If'

    print("\n=== Testing parse_comparison_expression ===")
    result3 = parser3.parse_comparison_expression()
    print("Result:", result3, type(result3))

except Exception as e:
    print("Parse error:", e)
    import traceback
    traceback.print_exc()
