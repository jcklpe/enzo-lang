# tokenizer.py -- Enzo language tokenizer/lexer
import re
from typing import List, Tuple, Optional, Iterator, NamedTuple
from src.error_handling import EnzoParseError

class Token(NamedTuple):
    type: str
    value: str
    start: int
    end: int

TOKEN_SPEC = [
    ("COLON_GT", r":>"),
    ("LT_COLON", r"<:"),
    ("LE", r"<="),
    ("GE", r">="),
    ("EQ", r"=="),
    ("NE", r"!="),
    ("LPAR", r"\("),
    ("RPAR", r"\)"),
    ("LBRACK", r"\["),
    ("RBRACK", r"\]"),
    ("LBRACE", r"\{"),
    ("RBRACE", r"\}"),
    ("COMMA", r","),
    ("SEMICOLON", r";"),
    ("COLON", r":"),
    ("DOT", r"\."),
    ("PLUS", r"\+"),
    ("NUMBER_TOKEN",   r"-?\d+(?:\.\d+)?"),  # <-- moved above MINUS
    ("MINUS", r"-"),
    ("STAR", r"\*"),
    ("SLASH", r"/"),
    ("LT", r"<"),
    ("GT", r">"),
    ("EQ_SINGLE", r"="),
    ("BANG", r"!"),
    ("AT", r"@"),
    ("TEXT_TOKEN", r'"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\''),
    # Allow dashes in variable names after the first character for both $-prefixed and non-prefixed
    ("KEYNAME",      r"\$[a-zA-Z0-9_-]+|[a-zA-Z_][a-zA-Z0-9_-]*"),
    ("NEWLINE",      r"\n"),
    ("WHITESPACE",   r"[ \t]+"),
    ("COMMENT",      r"//.*"),
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
                raise EnzoParseError(f"Unexpected character: {code[pos]!r} at {pos}")
            typ = m.lastgroup
            val = m.group(typ)
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
