# Debug parser with more detail
import sys
sys.path.insert(0, 'src')

from src.enzo_parser.parser import parse
from src.enzo_parser.tokenizer import Tokenizer

# Let's debug the full If statement parsing
code = '''$status: "ready";
If $status, (
    "Ready!";
);'''

print("Debugging If statement parsing")
print("Code:", repr(code))

try:
    # Let's manually step through the parser
    from src.enzo_parser.parser import Parser
    parser = Parser(code)

    # Parse the first statement (binding)
    first_stmt = parser.parse_statement()
    print("First statement:", type(first_stmt).__name__, first_stmt)

    # Parse the If statement
    if_stmt = parser.parse_statement()
    print("If statement:", type(if_stmt).__name__)
    print("  condition:", if_stmt.condition)
    print("  then_block:", if_stmt.then_block)
    print("  else_block:", if_stmt.else_block)

except Exception as e:
    print("Parse error:", e)
    import traceback
    traceback.print_exc()
