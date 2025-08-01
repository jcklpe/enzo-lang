#!/usr/bin/env python3

# Analyze the parser to understand where arithmetic is allowed

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Check where arithmetic parsing happens in different contexts
with open('src/enzo_parser/parser.py', 'r') as f:
    content = f.read()

print("=== PARSER ARITHMETIC CONTEXTS ANALYSIS ===")

# Look for arithmetic parsing contexts
contexts = [
    ('parse_assignment', 'Assignment context'),
    ('parse_rebinding', 'Rebinding context'),
    ('parse_comparison', 'Comparison context'),
    ('parse_arithmetic', 'Arithmetic context'),
    ('parse_expression', 'Expression context'),
    ('parse_statement', 'Statement context'),
    ('parse_atom', 'Atom context'),
    ('parse_primary', 'Primary context'),
]

for func_name, desc in contexts:
    if func_name in content:
        print(f"✅ Found {desc}: {func_name}")
        # Find the function definition
        start = content.find(f"def {func_name}")
        if start != -1:
            # Find first few lines to understand the logic
            end = content.find("\n    def ", start + 1)
            if end == -1:
                end = start + 800
            snippet = content[start:end][:600]
            print(f"   Logic preview:\n{snippet[:400]}...\n")
    else:
        print(f"❌ Missing {desc}")

print("\n=== CHECKING FOR ARITHMETIC NODE CREATION ===")
# Look for where arithmetic AST nodes are created
arithmetic_nodes = [
    'AddNode',
    'SubNode',
    'MulNode',
    'DivNode'
]

for node in arithmetic_nodes:
    occurrences = content.count(node)
    if occurrences > 0:
        print(f"'{node}' appears {occurrences} times in parser")

        # Find where it's created
        import_start = content.find(f"from src.enzo_parser.ast_nodes import")
        if import_start != -1:
            import_end = content.find("\n", import_start)
            imports = content[import_start:import_end]
            if node in imports:
                print(f"  - {node} is imported")

        # Find creation patterns
        creation_patterns = [f"{node}(", f"return {node}"]
        for pattern in creation_patterns:
            if pattern in content:
                print(f"  - Found creation pattern: {pattern}")

print("\n=== CHECKING ASSIGNMENT/REBINDING LOGIC ===")
# Look specifically at assignment and rebinding to see if they handle arithmetic specially
assignment_funcs = ['parse_assignment', 'parse_rebinding', 'parse_bind_or_rebind']
for func in assignment_funcs:
    if func in content:
        start = content.find(f"def {func}")
        if start != -1:
            end = content.find("\n    def ", start + 1)
            if end == -1:
                end = start + 1000
            func_content = content[start:end]

            # Look for arithmetic handling
            if any(term in func_content for term in ['arithmetic', 'expression', 'AddNode', 'parse_atom']):
                print(f"\n{func} handles arithmetic:")
                print(func_content[:500] + "...")
