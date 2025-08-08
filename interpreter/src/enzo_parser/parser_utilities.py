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

    # If no line info, try to extract the line containing the token using start position
    if hasattr(token, 'start') and token.start is not None and src:
        # Find which line contains this character position
        current_pos = 0
        for line_num, line in enumerate(src_lines):
            line_end = current_pos + len(line) + 1  # +1 for newline
            if current_pos <= token.start < line_end:
                return line
            current_pos = line_end

    return src_lines[0] if src_lines else src

def peek(tokens, pos):
    return tokens[pos] if pos < len(tokens) else None

def advance(tokens, pos):
    pos += 1
    return tokens[pos-1], pos

def synchronize_to_next_statement(parser):
    # Skip tokens until we find a likely statement boundary or the start of a new function atom
    from src.runtime_helpers import log_debug
    while parser.peek():
        t = parser.peek()
        log_debug(f"[sync] pos={parser.pos}, token={t}")
        # Stop at a semicolon, comma, closing paren/bracket/brace, or opening paren at start of line
        if t.type in ("SEMICOLON", "COMMA", "RPAR", "RBRACK", "RBRACE"):
            log_debug(f"[sync] Stopping at token type {t.type} at pos={parser.pos}")
            parser.advance()
            break
        if t.type == "LPAR":
            log_debug(f"[sync] Stopping at LPAR at pos={parser.pos}")
            # Optionally, check if this is at the start of a line (could use token position)
            break
        parser.advance()
        log_debug(f"[sync] Advanced to pos={parser.pos}")

def expect(parser, type_, scan_ahead=10):
    t = parser.peek()
    if not t or t.type != type_:
        # Scan ahead up to scan_ahead tokens for the expected type
        found = False
        for i in range(1, scan_ahead+1):
            lookahead = parser.peek() if i == 1 else (parser.tokens[parser.pos + i - 1] if parser.pos + i - 1 < len(parser.tokens) else None)
            if lookahead and lookahead.type == type_:
                # Advance parser.pos to the found token
                parser.pos += i - 1
                found = True
                break
        if not found:
            prev = parser.tokens[parser.pos - 1] if parser.pos > 0 else None
            line = getattr(prev, "line", 1) if prev else 1
            column = getattr(prev, "end", 0) + 1 if prev else 1
            if type_ == "RPAR":
                synchronize_to_next_statement(parser)
                raise EnzoParseError(error_message_unmatched_parenthesis(), line=line, column=column, code_line=parser._get_code_line(prev))
            elif type_ == "RBRACK":
                synchronize_to_next_statement(parser)
                raise EnzoParseError(error_message_unmatched_bracket(), line=line, column=column, code_line=parser._get_code_line(prev))
            elif type_ == "RBRACE":
                synchronize_to_next_statement(parser)
                raise EnzoParseError(error_message_unmatched_brace(), line=line, column=column, code_line=parser._get_code_line(prev))
            else:
                synchronize_to_next_statement(parser)
                raise EnzoParseError(error_message_expected_type(type_, t), line=line, column=column, code_line=parser._get_code_line(prev))
    return parser.advance()
