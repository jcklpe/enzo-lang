# Utility functions for Enzo parser

from src.error_handling import EnzoParseError
from src.error_messaging import (
    error_message_expected_type,
    error_message_unexpected_token,
    error_message_unmatched_parenthesis,
    error_message_unmatched_bracket,
    error_message_unmatched_brace,
)

def get_code_line(src_lines, token, src):
    if hasattr(token, 'line') and token.line is not None:
        line_num = token.line
        if 1 <= line_num <= len(src_lines):
            return src_lines[line_num - 1]
    return src_lines[0] if src_lines else src

def peek(tokens, pos):
    return tokens[pos] if pos < len(tokens) else None

def advance(tokens, pos):
    pos += 1
    return tokens[pos-1], pos

def expect(parser, type_):
    t = parser.peek()
    if not t or t.type != type_:
        prev = parser.tokens[parser.pos - 1] if parser.pos > 0 else None
        line = getattr(prev, "line", 1) if prev else 1
        column = getattr(prev, "end", 0) + 1 if prev else 1
        if type_ == "RPAR":
            raise EnzoParseError(error_message_unmatched_parenthesis(), line=line, column=column, code_line=parser._get_code_line(prev))
        elif type_ == "RBRACK":
            raise EnzoParseError(error_message_unmatched_bracket(), line=line, column=column, code_line=parser._get_code_line(prev))
        elif type_ == "RBRACE":
            raise EnzoParseError(error_message_unmatched_brace(), line=line, column=column, code_line=parser._get_code_line(prev))
        else:
            raise EnzoParseError(error_message_expected_type(type_, t), line=line, column=column, code_line=parser._get_code_line(prev))
    return parser.advance()
