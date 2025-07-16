#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.enzo_parser.parser import Parser

def test_complex_bracket():
    code = '[$age17, $fav-color17 -> $color17]:> $person17[];'
    parser = Parser(code)

    print(f"Testing: {code}")
    print("\nTokens:")
    for i, token in enumerate(parser.tokens):
        print(f"{i}: {token.type} = '{token.value}'")

    print("\nTesting detection logic:")
    parser.pos = 0  # Reset to start

    if parser.peek() and parser.peek().type == "LBRACK":
        print("✓ Found LBRACK at start")
        pos = 1
        found_keyname = False
        found_arrow_or_comma = False
        found_rbrack = False
        found_rebind_rightward = False

        while parser.peek(pos) and pos < 30:
            token = parser.peek(pos)
            print(f"  pos {pos}: {token.type} = '{token.value}'")

            if token.type == "KEYNAME" and not found_keyname:
                found_keyname = True
                print(f"    → found_keyname = True")
            elif token.type in ["COMMA", "ARROW"] and found_keyname:
                found_arrow_or_comma = True
                print(f"    → found_arrow_or_comma = True")
            elif token.type == "RBRACK" and found_arrow_or_comma:
                found_rbrack = True
                print(f"    → found_rbrack = True")
            elif token.type == "REBIND_RIGHTWARD" and found_rbrack:
                found_rebind_rightward = True
                print(f"    → found_rebind_rightward = True")
                break
            elif token.type in ["SEMICOLON", "NEWLINE", "RBRACE"]:
                print(f"    → End of statement")
                break
            pos += 1

        print(f"\nFinal detection result: found_rebind_rightward = {found_rebind_rightward}")

        if found_rebind_rightward:
            print("✓ Should call parse_complex_bracket_destructuring()")
            try:
                parser.pos = 0  # Reset
                result = parser.parse_complex_bracket_destructuring()
                print(f"✓ Complex bracket parsing successful: {type(result).__name__}")
            except Exception as e:
                print(f"✗ Complex bracket parsing failed: {e}")
        else:
            print("✗ Detection failed - would not call parse_complex_bracket_destructuring()")

    print("\nTesting full parsing:")
    try:
        parser.pos = 0  # Reset
        result = parser.parse()
        print(f"✓ Full parsing successful: {len(result.statements)} statements")
    except Exception as e:
        print(f"✗ Full parsing failed: {e}")

if __name__ == "__main__":
    test_complex_bracket()
