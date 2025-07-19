#!/usr/bin/env python3

# Simple test to check imports
import sys
import os

print("Current working directory:", os.getcwd())
print("Python path:", sys.path)

try:
    print("Testing basic import...")
    import src.enzo_parser.ast_nodes as ast_nodes
    print("✅ Basic import successful")

    print("Available classes:")
    classes = [name for name in dir(ast_nodes) if not name.startswith('_') and isinstance(getattr(ast_nodes, name), type)]
    for cls in sorted(classes):
        print(f"  - {cls}")

    print("\nTesting specific imports...")
    try:
        from src.enzo_parser.ast_nodes import IfStatement
        print("✅ IfStatement imported")
    except ImportError as e:
        print(f"❌ IfStatement import failed: {e}")

    try:
        from src.enzo_parser.ast_nodes import ComparisonExpression
        print("✅ ComparisonExpression imported")
    except ImportError as e:
        print(f"❌ ComparisonExpression import failed: {e}")

    # Check if classes are actually defined
    print("\nClass definitions check:")
    if hasattr(ast_nodes, 'IfStatement'):
        print("✅ IfStatement exists in module")
    else:
        print("❌ IfStatement does not exist in module")

    if hasattr(ast_nodes, 'ComparisonExpression'):
        print("✅ ComparisonExpression exists in module")
    else:
        print("❌ ComparisonExpression does not exist in module")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
