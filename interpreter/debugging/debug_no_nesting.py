#!/usr/bin/env python3

# Debug the "NO NESTING" test case specifically
test_line = "/' This outer comment ends here '/ \"and this text is not in a comment.\"; '/ // prints \"and this text is not in a comment.\""

print("Test line:")
print(repr(test_line))
print(f"Length: {len(test_line)}")
print()

print("Character by character:")
for i, char in enumerate(test_line):
    print(f"{i:2d}: {repr(char)}")
print()

print("Position 73:")
if len(test_line) > 73:
    print(f"Character at 73: {repr(test_line[73])}")
    print(f"Context around 73: {repr(test_line[70:77])}")
else:
    print("Position 73 is beyond string length")

print("\nAnalyzing the expected behavior:")
print("1. /' This outer comment ends here '/ -- This should be a complete block comment")
print("2. \"and this text is not in a comment.\" -- This should be a text literal")
print("3. ; -- Semicolon")
print("4. '/ -- This should be an error (unexpected single quote followed by slash)")
print("   The test expects this to fail with 'Unexpected character' error")
