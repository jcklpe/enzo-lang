# Debug the parsing chain in detail
import sys
sys.path.insert(0, 'src')

from src.enzo_parser.parser import Parser

code = 'If $status, ("Ready!";);'

print("Debugging the full parsing chain")

try:
    parser = Parser(code)

    # Manually follow the chain
    print("Current token:", parser.peek())
    parser.advance()  # consume 'If'
    print("After consuming If, current token:", parser.peek())

    # Call parse_comparison which should call the chain
    print("\n=== Calling parse_comparison ===")
    result = parser.parse_comparison()
    print("parse_comparison result:", result, type(result))

    # Let's manually trace the chain with a fresh parser
    print("\n=== Manual chain tracing ===")
    parser2 = Parser('$status')
    print("Parsing just '$status' with fresh parser")
    print("Token:", parser2.peek())

    print("Calling parse_atom...")
    atom_result = parser2.parse_atom()
    print("parse_atom result:", atom_result, type(atom_result))

except Exception as e:
    print("Parse error:", e)
    import traceback
    traceback.print_exc()
