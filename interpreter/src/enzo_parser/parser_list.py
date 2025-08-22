from src.enzo_parser.ast_nodes import ListAtom, ListKeyValue, ListInterpolation
from src.error_handling import EnzoParseError
from src.enzo_parser.parser_utilities import expect
import re

def parse_list_atom(parser):
    expect(parser, "LBRACK")
    elements = []
    saw_item = False
    has_key_value_pairs = False  # Track if this list contains key-value pairs
    t_start = parser.peek()
    code_line = parser._get_code_line(t_start) if t_start else None

    while True:
        t = parser.peek()
        if t and t.type == "RBRACK":
            parser.advance()
            break
        if t and t.type == "COMMA":
            t2 = parser.tokens[parser.pos + 1] if parser.pos + 1 < len(parser.tokens) else None
            # Choose error messages based on whether we have key-value pairs
            if has_key_value_pairs:
                from src.error_messaging import error_message_empty_table_comma, error_message_leading_comma_table, error_message_double_comma_table
                if t2 and t2.type == "RBRACK" and not saw_item:
                    raise EnzoParseError(error_message_empty_table_comma(), code_line=parser._get_code_line(t))
                if not saw_item:
                    raise EnzoParseError(error_message_leading_comma_table(), code_line=parser._get_code_line(t))
                raise EnzoParseError(error_message_double_comma_table(), code_line=parser._get_code_line(t))
            else:
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
            raise EnzoParseError(error_message_unmatched_bracket(), code_line=parser._get_code_line(t))        # Check for list interpolation syntax: <$variable>
        if t.type == "LT":
            # This is a list interpolation: <expression>
            parser.advance()  # consume '<'
            expression = parser.parse_value_expression()
            # Expect '>' to close the interpolation
            gt_token = parser.peek()
            if gt_token and gt_token.type == "GT":
                parser.advance()  # consume '>'
                elements.append(ListInterpolation(expression, code_line=parser._get_code_line(t)))
            else:
                from src.error_messaging import error_message_unexpected_token
                raise EnzoParseError(f"error: expected '>' to close list interpolation", code_line=parser._get_code_line(gt_token) if gt_token else None)
        # Check for key-value pair (@keyname: value or keyname: value)
        elif t.type == "AT":
            # Look ahead to see if this is @keyname: pattern
            t2 = parser.tokens[parser.pos + 1] if parser.pos + 1 < len(parser.tokens) else None
            t3 = parser.tokens[parser.pos + 2] if parser.pos + 2 < len(parser.tokens) else None
            if t2 and t2.type == "KEYNAME" and t3 and t3.type == "BIND":
                # This is @keyname: value pattern
                has_key_value_pairs = True  # Mark that we have key-value pairs
                parser.advance()  # consume AT token
                keyname = parser.advance().value  # consume KEYNAME token
                parser.advance()  # consume BIND token

                # Validate keyname - must not be purely numeric
                if _is_purely_numeric(keyname):
                    raise EnzoParseError(f"error: purely numeric keynames are not allowed: {keyname}", code_line=parser._get_code_line(t))

                value = parser.parse_value_expression()
                elements.append(ListKeyValue(keyname, value, code_line=parser._get_code_line(t)))
            else:
                # This is a regular @ reference element
                elements.append(parser.parse_value_expression())
        elif t.type == "KEYNAME":
            # Look ahead to see if this is a key-value pair
            t2 = parser.tokens[parser.pos + 1] if parser.pos + 1 < len(parser.tokens) else None
            if t2 and t2.type == "BIND":
                # Check if this is $variable: pattern (which should error)
                if t.value.startswith('$'):
                    from src.error_messaging import error_message_dollar_in_assignment
                    raise EnzoParseError(error_message_dollar_in_assignment(), code_line=parser._get_code_line(t))

                # This is a key-value pair
                has_key_value_pairs = True  # Mark that we have key-value pairs
                keyname = parser.advance().value
                parser.advance()  # consume BIND token

                # Validate keyname - must not be purely numeric
                if _is_purely_numeric(keyname):
                    raise EnzoParseError(f"error: purely numeric keynames are not allowed: {keyname}", code_line=parser._get_code_line(t))

                value = parser.parse_value_expression()
                elements.append(ListKeyValue(keyname, value, code_line=parser._get_code_line(t)))
            else:
                # This is a regular element (keyname without :)
                elements.append(parser.parse_value_expression())
        elif t.type == "NUMBER_TOKEN":
            # Check if this number is followed by BIND (which would be invalid)
            t2 = parser.tokens[parser.pos + 1] if parser.pos + 1 < len(parser.tokens) else None
            if t2 and t2.type == "BIND":
                # This is an invalid numeric keyname
                raise EnzoParseError(f"error: purely numeric keynames are not allowed: {t.value}", code_line=parser._get_code_line(t))
            else:
                # Regular number element
                elements.append(parser.parse_value_expression())
        else:
            # Regular element
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
                # Choose error message based on whether we have key-value pairs
                if has_key_value_pairs:
                    from src.error_messaging import error_message_double_comma_table
                    raise EnzoParseError(error_message_double_comma_table(), code_line=parser._get_code_line(t2))
                else:
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

def _is_purely_numeric(keyname):
    """Check if a keyname is purely numeric (integer or float)."""
    try:
        float(keyname)
        return True
    except ValueError:
        return False
