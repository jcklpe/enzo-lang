from src.enzo_parser.ast_nodes import ListAtom
from src.error_handling import EnzoParseError
from src.enzo_parser.parser_utilities import expect

def parse_list_atom(parser):
    expect(parser, "LBRACK")
    elements = []
    saw_item = False
    t_start = parser.peek()
    code_line = parser._get_code_line(t_start) if t_start else None
    while True:
        t = parser.peek()
        if t and t.type == "RBRACK":
            parser.advance()
            break
        if t and t.type == "COMMA":
            t2 = parser.tokens[parser.pos + 1] if parser.pos + 1 < len(parser.tokens) else None
            from src.error_messaging import error_message_empty_list_comma, error_message_excess_leading_comma, error_message_double_comma
            if t2 and t2.type == "RBRACK" and not saw_item:
                raise EnzoParseError(error_message_empty_list_comma(), code_line=parser._get_code_line(t))
            if not saw_item:
                raise EnzoParseError(error_message_excess_leading_comma(), code_line=parser._get_code_line(t))
            raise EnzoParseError(error_message_double_comma(), code_line=parser._get_code_line(t))
        if t is None:
            from src.error_messaging import error_message_unmatched_bracket
            raise EnzoParseError(error_message_unmatched_bracket(), code_line=None)
        if t.type == "SEMICOLON":
            from src.error_messaging import error_message_unmatched_bracket
            raise EnzoParseError(error_message_unmatched_bracket(), code_line=parser._get_code_line(t))
        elements.append(parser.parse_value_expression())
        saw_item = True
        t = parser.peek()
        if t and t.type == "COMMA":
            parser.advance()
            t2 = parser.peek()
            if t2 and t2.type == "RBRACK":
                parser.advance()
                break
            if t2 and t2.type == "COMMA":
                from src.error_messaging import error_message_double_comma
                raise EnzoParseError(error_message_double_comma(), code_line=parser._get_code_line(t2))
        elif t and t.type == "RBRACK":
            parser.advance()
            break
        elif t:
            from src.error_messaging import error_message_unmatched_bracket
            raise EnzoParseError(error_message_unmatched_bracket(), code_line=parser._get_code_line(t))
        else:
            from src.error_messaging import error_message_unmatched_bracket
            raise EnzoParseError(error_message_unmatched_bracket(), code_line=None)
    return ListAtom(elements, code_line=code_line)
