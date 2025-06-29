from .ast_nodes import TableAtom
from src.error_handling import EnzoParseError
from .parser_utilities import expect

def parse_table_atom(parser):
    expect(parser, "LBRACE")
    items = []
    trailing_comma = False
    t_start = parser.peek()
    code_line = parser._get_code_line(t_start) if t_start else None
    if parser.peek() and not (parser.peek().type == "RBRACE"):
        property_value_pairs = []
        saw_item = False
        while True:
            t = parser.peek()
            if t is None:
                from src.error_messaging import error_message_unmatched_brace
                raise EnzoParseError(error_message_unmatched_brace(), code_line=parser._get_code_line(t))
            if t.type == "RBRACE":
                if not saw_item and trailing_comma:
                    from src.error_messaging import error_message_empty_table_comma
                    raise EnzoParseError(error_message_empty_table_comma(), code_line=parser._get_code_line(t))
                break
            if t.type == "COMMA":
                t2 = parser.tokens[parser.pos + 1] if parser.pos + 1 < len(parser.tokens) else None
                from src.error_messaging import error_message_leading_comma_table, error_message_double_comma_table, error_message_empty_table_comma
                if not saw_item:
                    if t2 and t2.type == "RBRACE":
                        raise EnzoParseError(error_message_empty_table_comma(), code_line=parser._get_code_line(t))
                    else:
                        raise EnzoParseError(error_message_leading_comma_table(), code_line=parser._get_code_line(t))
                if t2 and t2.type == "COMMA":
                    raise EnzoParseError(error_message_double_comma_table(), code_line=parser._get_code_line(t2))
                parser.advance()
                trailing_comma = True
                continue
            if t.type != "KEYNAME":
                from src.error_messaging import error_message_unmatched_brace
                raise EnzoParseError(error_message_unmatched_brace(), code_line=parser._get_code_line(t))
            property_name = parser.expect("KEYNAME").value
            parser.expect("COLON")
            value = parser.parse_value_expression()
            property_value_pairs.append((property_name, value))
            saw_item = True
            t = parser.peek()
            if t and t.type == "COMMA":
                parser.advance()
                trailing_comma = True
                t2 = parser.peek()
                if t2 and t2.type == "COMMA":
                    from src.error_messaging import error_message_double_comma_table
                    raise EnzoParseError(error_message_double_comma_table(), code_line=parser._get_code_line(t2))
            else:
                trailing_comma = False
        # Overwrite duplicate properties: last one wins, preserve order of last occurrence
        seen = {}
        ordered = []
        for prop, val in property_value_pairs:
            if prop in seen:
                ordered = [pair for pair in ordered if pair[0] != prop]
            seen[prop] = val
            ordered.append((prop, val))
        items = ordered
    t = parser.peek()
    if not t or t.type != "RBRACE":
        from src.error_messaging import error_message_unmatched_brace
        raise EnzoParseError(error_message_unmatched_brace(), code_line=parser._get_code_line(t))
    parser.advance()
    return TableAtom(items, code_line=code_line)
