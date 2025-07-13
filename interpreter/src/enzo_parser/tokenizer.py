# tokenizer.py -- Enzo language tokenizer/lexer
import re
from typing import List, Tuple, Optional, Iterator, NamedTuple
from src.error_handling import EnzoParseError
from src.error_messaging import error_message_unexpected_character

class Token(NamedTuple):
    type: str
    value: str
    start: int
    end: int

TOKEN_SPEC = [
    ("REBIND_RIGHTWARD", r":>"),
    ("REBIND_LEFTWARD", r"<:"),
    ("LE", r"<="),
    ("GE", r">="),
    ("EQ", r"=="),
    ("NE", r"!="),
    ("BLUEPRINT_START", r"<\["),    # <[ - Must come before LT and LBRACK
    ("BLUEPRINT_END", r"\]>"),      # ]> - Must come before RBRACK and GT
    ("LPAR", r"\("),
    ("RPAR", r"\)"),
    ("LBRACK", r"\["),
    ("RBRACK", r"\]"),
    ("LBRACE", r"\{"),
    ("RBRACE", r"\}"),
    ("COMMA", r","),
    ("SEMICOLON", r";"),
    ("BIND", r":"),
    ("DOT", r"\."),
    ("PLUS", r"\+"),
    ("NUMBER_TOKEN",   r"-?\d+(?:\.\d+)?"),  # <-- moved above MINUS
    ("MINUS", r"-"),
    ("STAR", r"\*"),
    ("COMMENT", r"//.*"),  # Move COMMENT before SLASH to match "//" properly
    ("SLASH", r"/"),
    ("AND", r"\band\b"),            # \b for word boundaries
    ("OR", r"\bor\b"),              # \b for word boundaries
    ("VARIANTS", r"\bvariants\b"),  # \b for word boundaries
    ("LT", r"<"),
    ("GT", r">"),
    ("EQ_SINGLE", r"="),
    ("BANG", r"!"),
    ("AT", r"@"),
    ("TEXT_TOKEN", r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\''),
    ("RETURN", r"return"),  # Add RETURN keyword before KEYNAME
    ("THEN", r"then"),      # Add THEN keyword before KEYNAME
    ("PARAM", r"param"),    # Add PARAM keyword before KEYNAME
    ("THIS", r"\$this"),    # Add $this as dedicated reserved token
    # Allow dashes in variable names after the first character for both $-prefixed and non-prefixed
    ("KEYNAME",      r"\$[a-zA-Z0-9_-]+|[a-zA-Z_][a-zA-Z0-9_-]*"),
    ("NEWLINE",      r"\n"),
    ("WHITESPACE",   r"[ \t]+"),
]

TOKEN_REGEX = re.compile(
    "|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPEC)
)

class Tokenizer:
    def __init__(self, code: str):
        self.code = code
        self.pos = 0
        self.tokens: List[Token] = []

    def tokenize(self) -> List[Token]:
        code = self.code
        pos = 0
        tokens = []
        while pos < len(code):
            m = TOKEN_REGEX.match(code, pos)
            if not m:
                # Special handling: if we see a dot followed by a number (e.g. .2), treat as DOT then NUMBER_TOKEN
                if code[pos] == '.' and pos + 1 < len(code) and code[pos+1].isdigit():
                    tokens.append(Token('DOT', '.', pos, pos+1))
                    # Now match the number after the dot, but only up to the next dot (for chained indices)
                    num_match = re.match(r'(\d+)', code[pos+1:])
                    if num_match:
                        num_val = num_match.group(0)
                        tokens.append(Token('NUMBER_TOKEN', num_val, pos+1, pos+1+len(num_val)))
                        pos += 1 + len(num_val)
                        continue
                raise EnzoParseError(error_message_unexpected_character(code[pos], pos))
            typ = m.lastgroup
            val = m.group(typ)
            # Patch: If this is a NUMBER_TOKEN and the previous token was DOT, and the number contains a dot (float), split it into multiple tokens
            if typ == "NUMBER_TOKEN" and '.' in val and tokens and tokens[-1].type == 'DOT':
                # Split at each dot for chained indices, e.g. .2.1 -> DOT, NUMBER_TOKEN(2), DOT, NUMBER_TOKEN(1)
                parts = val.split('.')
                for i, part in enumerate(parts):
                    if i > 0:
                        tokens.append(Token('DOT', '.', pos, pos+1))
                        pos += 1  # move past the dot
                    tokens.append(Token('NUMBER_TOKEN', part, pos, pos+len(part)))
                    pos += len(part)
                continue
            if typ == "WHITESPACE" or typ == "COMMENT":
                pass
            elif typ == "NEWLINE":
                tokens.append(Token("NEWLINE", val, pos, m.end()))
            else:
                tokens.append(Token(typ, val, pos, m.end()))
            pos = m.end()
        return tokens

# Example usage:
# tokenizer = Tokenizer("x = 42\nfoo($bar, 3.14)")
# tokens = tokenizer.tokenize()
# for t in tokens:
#     print(t)

if __name__ == "__main__":
    # Simple test for the tokenizer
    sample = '''x = 42\nfoo($bar, 3.14)\ntext = "hello, world!"\n# comment line\n'escaped \\'string\\''\n'''
    tokenizer = Tokenizer(sample)
    tokens = tokenizer.tokenize()
    for t in tokens:
        print(t)
