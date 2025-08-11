#!/usr/bin/env python3

# Debug AST node imports
print("Testing AST node imports...")

try:
    # Import the module
    import src.enzo_parser.ast_nodes as ast_nodes
    print("✅ Module imported successfully")

    # Check if IfStatement exists
    if hasattr(ast_nodes, 'IfStatement'):
        print("✅ IfStatement found")
        print(f"   Type: {type(ast_nodes.IfStatement)}")
    else:
        print("❌ IfStatement NOT found")

    # Show all available classes
    print("\nAll non-private attributes:")
    attrs = [attr for attr in dir(ast_nodes) if not attr.startswith('_')]
    for attr in sorted(attrs):
        obj = getattr(ast_nodes, attr)
        print(f"  {attr}: {type(obj)}")

    # Try to read the source file and check the end
    with open('src/enzo_parser/ast_nodes.py', 'r') as f:
        lines = f.readlines()

    print(f"\nFile has {len(lines)} lines")
    print("Last 5 lines:")
    for i, line in enumerate(lines[-5:], start=len(lines)-4):
        print(f"  {i:3d}: {line.rstrip()}")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
