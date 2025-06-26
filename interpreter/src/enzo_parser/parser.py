# Recursive-descent parser skeleton for Enzo
# This is a scaffold for a context-aware parser

from .ast_nodes import *
from .tokenizer import Tokenizer
from src.error_handling import EnzoParseError
from src.error_messaging import error_message_expected_type, error_message_unexpected_token

def parse(src):
    tokens = Tokenizer(src).tokenize()
    tokens = [t for t in tokens if t.type not in ("NEWLINE", "COMMENT", "SKIP")]
    pos = 0
    def peek():
        return tokens[pos] if pos < len(tokens) else None
    def advance():
        nonlocal pos
        pos += 1
        return tokens[pos-1]
    def expect(type_):
        t = peek()
        if not t or t.type != type_:
            raise EnzoParseError(error_message_expected_type(type_, t))
        return advance()
    def parse_function_atom():
        # Assumes '(' already consumed
        items = []
        sep_seen = False
        while peek() and not (peek().type == "OPERATOR" and peek().value == ")"):
            t = peek()
            if t.type == "KEYNAME":
                name = advance().value
                if peek() and peek().type == "OPERATOR" and peek().value == ":":
                    advance()
                    if peek() and not (peek().type == "OPERATOR" and peek().value in (",", ";", ")")):
                        value_expression = parse_value_expression()
                        items.append(Binding(name, value_expression))
                    else:
                        items.append(Binding(name, None))
                else:
                    items.append(name)  # Just a keyname value expression (param)
            else:
                items.append(parse_value_expression())
            if peek() and peek().type == "OPERATOR" and peek().value in (",", ";"):
                sep_seen = True
                advance()
        expect("OPERATOR")  # ')'
        # Partition items into params, bindings, statements
        params = []
        local_vars = []
        body = []
        for item in items:
            if isinstance(item, Binding) and item.value is None:
                params.append(item.name)
            elif isinstance(item, Binding):
                local_vars.append(item)
            elif isinstance(item, str):
                params.append(item)
            else:
                body.append(item)
        has_newline = False  # Not tracked yet
        return FunctionAtom(params, local_vars, body)

    def parse_list_atom():
        expect("OPERATOR")  # '['
        elements = []
        trailing_comma = False
        if peek() and not (peek().type == "OPERATOR" and peek().value == "]"):
            while True:
                elements.append(parse_value_expression())
                if peek() and peek().type == "OPERATOR" and peek().value == ",":
                    advance()
                    trailing_comma = True
                else:
                    trailing_comma = False
                    break
        expect("OPERATOR")  # ']'
        return ListAtom(elements)

    def parse_table_atom():
        expect("OPERATOR")  # '{'
        items = []
        trailing_comma = False
        if peek() and not (peek().type == "OPERATOR" and peek().value == "}"):
            while True:
                key = expect("KEYNAME").value
                expect("OPERATOR")  # ':'
                value = parse_value_expression()
                items.append((key, value))
                if peek() and peek().type == "OPERATOR" and peek().value == ",":
                    advance()
                    trailing_comma = True
                else:
                    trailing_comma = False
                    break
        expect("OPERATOR")  # '}'
        return TableAtom(items)

    def parse_postfix(base):
        while peek() and peek().type == "OPERATOR" and peek().value.startswith("."):
            operator_value = peek().value
            # Defensive: only check operator_value[1] or operator_value[2] if long enough
            if len(operator_value) > 1 and (operator_value[1:].isdigit() or (len(operator_value) > 2 and operator_value[1] == '-' and operator_value[2:].isdigit())):
                advance()
                base = Invoke(base, [NumberAtom(int(operator_value[1:]))])
            elif operator_value.startswith(".$") and len(operator_value) > 2:
                advance()
                base = Invoke(base, [operator_value[2:]])  # keyname as string
            elif len(operator_value) > 1:
                advance()
                base = Invoke(base, [operator_value[1:]])  # property as string
            else:
                # Defensive: skip or break if operator_value is just "."
                break
        return base

    def parse_atom():
        t = peek()
        if not t:
            raise EnzoParseError("Unexpected end of input")
        if t.type == "NUMBER_TOKEN":
            advance()
            return NumberAtom(float(t.value) if "." in t.value else int(t.value))
        elif t.type == "TEXT_TOKEN":
            advance()
            val = t.value[1:-1].encode('utf-8').decode('unicode_escape')
            return TextAtom(val)
        elif t.type == "KEYNAME":
            advance()
            node = VarInvoke(t.value)
            node = parse_postfix(node)
            return node
        elif t.type == "OPERATOR" and t.value == "(":
            advance()  # consume '('
            # Look ahead: function atom or parenthesized expression?
            if peek() and peek().type == "KEYNAME" and pos + 1 < len(tokens) and tokens[pos + 1].type == "OPERATOR" and tokens[pos + 1].value == ":":
                node = parse_function_atom()
            else:
                node = parse_value_expression()
                expect("OPERATOR")  # ')'
            node = parse_postfix(node)
            return node
        elif t.type == "OPERATOR" and t.value == "[":
            node = parse_list_atom()
            node = parse_postfix(node)
            return node
        elif t.type == "OPERATOR" and t.value == "{":
            node = parse_table_atom()
            node = parse_postfix(node)
            return node
        else:
            raise EnzoParseError(error_message_unexpected_token(t))

    def parse_factor():
        node = parse_atom()
        node = parse_postfix(node)
        while peek() and peek().type == "OPERATOR" and peek().value in ("*", "/"):
            op = advance().value
            right = parse_atom()
            right = parse_postfix(right)
            if op == "*":
                node = MulNode(node, right)
            else:
                node = DivNode(node, right)
        return node

    def parse_term():
        node = parse_factor()
        while peek() and peek().type == "OPERATOR" and peek().value in ("+", "-"):
            op = advance().value
            right = parse_factor()
            if op == "+":
                node = AddNode(node, right)
            else:
                node = SubNode(node, right)
        return node

    def parse_value_expression():
        return parse_term()

    def parse_statement():
        t = peek()
        # 1. Handle $var: ..., $var <: ..., $var :> ...
        if t and t.type == "KEYNAME":
            name = t.value
            if pos + 1 < len(tokens):
                next_t = tokens[pos + 1]
                if next_t.type == "OPERATOR" and next_t.value == ":":
                    advance()  # KEYNAME
                    advance()  # ':'
                    if peek() and not (peek().type == "OPERATOR" and peek().value in (";", ",", ")")):
                        value = parse_value_expression()
                        return Binding(name, value)
                    else:
                        return Binding(name, None)
                elif next_t.type == "OPERATOR" and next_t.value == "<:":
                    advance()  # KEYNAME
                    advance()  # '<:'
                    value = parse_value_expression()
                    # Rebind is not yet an AST node, keep as tuple for now
                    return ("rebind", name, value)
                elif next_t.type == "OPERATOR" and next_t.value == ":>":
                    advance()  # KEYNAME
                    advance()  # ':>'
                    value = parse_value_expression()
                    return BindOrRebind(name, value)
        # 2. Handle expr1 :> expr2 (either side can be a variable, the other a value)
        expr1 = parse_value_expression()
        if peek() and peek().type == "OPERATOR" and peek().value == ":>":
            advance()  # ':>'
            expr2 = parse_value_expression()
            # Determine which side is the variable
            if isinstance(expr1, VarInvoke) and isinstance(expr2, VarInvoke):
                # Both are variables, ambiguous, error
                raise EnzoParseError("Ambiguous :> binding: both sides are variables")
            elif isinstance(expr1, VarInvoke):
                return BindOrRebind(expr1.name, expr2)
            elif isinstance(expr2, VarInvoke):
                return BindOrRebind(expr2.name, expr1)
            else:
                raise EnzoParseError(":> must have a variable on one side")
        # 3. Fallback: just a value expression
        return expr1

    def parse_statements():
        stmts = []
        while pos < len(tokens):
            stmts.append(parse_statement())
            if peek() and peek().type == "OPERATOR" and peek().value in (";",):
                advance()
            else:
                break
        return stmts

    def parse_block():
        stmts = parse_statements()
        if len(stmts) == 1:
            return stmts[0]
        else:
            return stmts

    ast = parse_block()
    if pos != len(tokens):
        raise EnzoParseError(error_message_unexpected_token(tokens[pos]))
    return ast

def parse_program(src):
    tokens = Tokenizer(src).tokenize()
    tokens = [t for t in tokens if t.type not in ("NEWLINE", "COMMENT", "SKIP")]
    global pos
    pos = 0
    def at_end():
        return pos >= len(tokens)
    statements = []
    while not at_end():
        stmt = parse_statement()
        statements.append(stmt)
        if peek() and peek().type == "OPERATOR" and peek().value in (";", ","):
            advance()
    return Program(statements)

# TODO: Implement parse_statement, parse_expr, parse_function_atom, etc.
# Each should take a context argument (e.g., 'top-level', 'binding', 'expression')
