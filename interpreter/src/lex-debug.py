#!/usr/bin/env python3
from pathlib import Path
from lark import Lark, Token

# --- Load your grammar
grammar_path = Path("src/grammar.lark")  # adjust if your path is different
grammar = grammar_path.read_text()
parser = Lark(grammar, parser="lalr", start="start")

# --- Put the exact function block you want to test
input_text = """
(
$x: 100;
$y: 100;
return($x + $y);
)
"""
print("=== TOKENS ===")
for tok in parser.lex(input_text):
    print(repr(tok))
