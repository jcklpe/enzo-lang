#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.enzo_parser.tokenizer import Tokenizer

# Test just the problematic section to see token boundaries
code = '''$goblinoid
  then take-damage1($this, 30)
    then If $this.health is less than 1, (
        set-status($this, "dead")
    )
  :> $goblinoid;

$goblinoid.health;  // should print 0
$goblinoid.status;  // should print "dead"

//= IF CONDITION WITH NESTED LIST INDEX ACCESS
$nested-list: [["zero", "one"], ["two", "three"]];'''

print("=== TOKENIZATION TEST ===")
tokenizer = Tokenizer(code)
tokens = tokenizer.tokenize()

print("All tokens:")
for i, token in enumerate(tokens):
    if token.type != "WHITESPACE":  # Skip whitespace for clarity
        print(f"{i:2d}: {token.type:15s} {repr(token.value)} at {token.start}-{token.end}")

print("\n=== LOOKING FOR COMMENT TOKEN ===")
comment_tokens = [t for t in tokens if t.type == "COMMENT"]
if comment_tokens:
    for token in comment_tokens:
        print(f"Found comment: {repr(token.value)} at {token.start}-{token.end}")
else:
    print("No comment tokens found!")

# Now let's see what the filtered tokens look like (what the parser sees)
filtered_tokens = [t for t in tokens if t.type not in ("NEWLINE", "COMMENT", "SKIP", "WHITESPACE")]
print(f"\n=== FILTERED TOKENS (what parser sees) ===")
for i, token in enumerate(filtered_tokens):
    print(f"{i:2d}: {token.type:15s} {repr(token.value)}")
