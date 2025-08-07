# Debug comparison parsing
import sys
sys.path.insert(0, 'src')

from src.enzo_parser.parser import Parser

code = 'If $status, ("Ready!";);'

print("Debugging condition parsing in If statement")

try:
    parser = Parser(code)

    # Manually step through the If parsing
    print("Current token:", parser.peek())
    parser.advance()  # consume 'If'
    print("After consuming If, current token:", parser.peek())

    # This is where parse_if_statement calls parse_comparison()
    condition = parser.parse_comparison()
    print("Parsed condition:", condition, type(condition))

    print("Current token after parsing condition:", parser.peek())

except Exception as e:
    print("Parse error:", e)
    import traceback
    traceback.print_exc()
