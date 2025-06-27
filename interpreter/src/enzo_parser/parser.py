# Recursive-descent parser skeleton for Enzo
# This is a scaffold for a context-aware parser

from .ast_nodes import *
from .tokenizer import Tokenizer
from src.error_handling import EnzoParseError
from src.error_messaging import error_message_expected_type, error_message_unexpected_token

class Parser:
    def __init__(self, src):
        self.tokens = Tokenizer(src).tokenize()
        self.tokens = [t for t in self.tokens if t.type not in ("NEWLINE", "COMMENT", "SKIP")]
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def advance(self):
        self.pos += 1
        return self.tokens[self.pos-1]

    def expect(self, type_):
        t = self.peek()
        if not t or t.type != type_:
            raise EnzoParseError(error_message_expected_type(type_, t))
        return self.advance()

    def parse_function_atom(self):
        self.expect("OPERATOR")  # '('
        # Look ahead: function definition or value expression?
        t = self.peek()
        if t and t.type == "KEYNAME":
            # Look ahead for KEYNAME : (function param or local var)
            save_pos = self.pos
            name = t.value
            self.advance()
            if self.peek() and self.peek().type == "OPERATOR" and self.peek().value == ":":
                # Function definition or local var
                self.pos = save_pos  # rewind
                items = []
                sep_seen = False
                while self.peek() and not (self.peek().type == "OPERATOR" and self.peek().value == ")"):
                    t = self.peek()
                    if t.type == "KEYNAME":
                        name = self.advance().value
                        if self.peek() and self.peek().type == "OPERATOR" and self.peek().value == ":":
                            self.advance()
                            if self.peek() and not (self.peek().type == "OPERATOR" and self.peek().value in (",", ";", ")")):
                                value_expression = self.parse_value_expression()
                                items.append(Binding(name, value_expression))
                            else:
                                items.append(Binding(name, None))
                        else:
                            items.append(name)
                    else:
                        items.append(self.parse_value_expression())
                    if self.peek() and self.peek().type == "OPERATOR" and self.peek().value in (",", ";"):
                        sep_seen = True
                        self.advance()
                self.expect("OPERATOR")  # ')'
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
                if not params and not local_vars and len(body) == 1:
                    return FunctionAtom([], [], body)
                return FunctionAtom(params, local_vars, body)
            else:
                # Not a function definition, treat as value expression
                self.pos = save_pos  # rewind
        # Not a function definition: parse a single value expression
        expr = self.parse_value_expression()
        self.expect("OPERATOR")  # ')'
        return FunctionAtom([], [], [expr])

    def parse_list_atom(self):
        self.expect("OPERATOR")  # '['
        elements = []
        trailing_comma = False
        if self.peek() and not (self.peek().type == "OPERATOR" and self.peek().value == "]"):
            while True:
                elements.append(self.parse_value_expression())
                if self.peek() and self.peek().type == "OPERATOR" and self.peek().value == ",":
                    self.advance()
                    trailing_comma = True
                else:
                    trailing_comma = False
                    break
        self.expect("OPERATOR")  # ']'
        return ListAtom(elements)

    def parse_table_atom(self):
        self.expect("OPERATOR")  # '{'
        items = []
        trailing_comma = False
        if self.peek() and not (self.peek().type == "OPERATOR" and self.peek().value == "}"):
            while True:
                key = self.expect("KEYNAME").value
                self.expect("OPERATOR")  # ':'
                value = self.parse_value_expression()
                items.append((key, value))
                if self.peek() and self.peek().type == "OPERATOR" and self.peek().value == ",":
                    self.advance()
                    trailing_comma = True
                else:
                    trailing_comma = False
                    break
        self.expect("OPERATOR")  # '}'
        return TableAtom(items)

    def parse_postfix(self, base):
        while self.peek() and self.peek().type == "OPERATOR" and self.peek().value.startswith("."):
            operator_value = self.peek().value
            if len(operator_value) > 1 and (operator_value[1:].isdigit() or (len(operator_value) > 2 and operator_value[1] == '-' and operator_value[2:].isdigit())):
                self.advance()
                base = Invoke(base, [NumberAtom(int(operator_value[1:]))])
            elif operator_value.startswith(".$") and len(operator_value) > 2:
                self.advance()
                base = Invoke(base, [operator_value[2:]])
            elif len(operator_value) > 1:
                self.advance()
                base = Invoke(base, [operator_value[1:]])
            else:
                break
        return base

    def parse_atom(self):
        t = self.peek()
        if not t:
            raise EnzoParseError("Unexpected end of input")
        if t.type == "NUMBER_TOKEN":
            self.advance()
            return NumberAtom(float(t.value) if "." in t.value else int(t.value))
        elif t.type == "TEXT_TOKEN":
            self.advance()
            val = t.value[1:-1].encode('utf-8').decode('unicode_escape')
            return TextAtom(val)
        elif t.type == "KEYNAME":
            self.advance()
            node = VarInvoke(t.value)
            node = self.parse_postfix(node)
            return node
        elif t.type == "OPERATOR" and t.value == "(":
            node = self.parse_function_atom()
            node = self.parse_postfix(node)
            return node
        elif t.type == "OPERATOR" and t.value == "[":
            node = self.parse_list_atom()
            node = self.parse_postfix(node)
            return node
        elif t.type == "OPERATOR" and t.value == "{":
            node = self.parse_table_atom()
            node = self.parse_postfix(node)
            return node
        else:
            raise EnzoParseError(error_message_unexpected_token(t))

    def parse_factor(self):
        node = self.parse_atom()
        node = self.parse_postfix(node)
        while self.peek() and self.peek().type == "OPERATOR" and self.peek().value in ("*", "/"):
            op = self.advance().value
            right = self.parse_atom()
            right = self.parse_postfix(right)
            if op == "*":
                node = MulNode(node, right)
            else:
                node = DivNode(node, right)
        return node

    def parse_term(self):
        node = self.parse_factor()
        while self.peek() and self.peek().type == "OPERATOR" and self.peek().value in ("+", "-"):
            op = self.advance().value
            right = self.parse_factor()
            if op == "+":
                node = AddNode(node, right)
            else:
                node = SubNode(node, right)
        return node

    def parse_value_expression(self):
        return self.parse_term()

    def parse_statement(self):
        t = self.peek()
        if t and t.type == "KEYNAME":
            name = t.value
            if self.pos + 1 < len(self.tokens):
                next_t = self.tokens[self.pos + 1]
                if next_t.type == "OPERATOR" and next_t.value == ":":
                    self.advance()
                    self.advance()
                    if self.peek() and not (self.peek().type == "OPERATOR" and self.peek().value in (";", ",", ")")):
                        value = self.parse_value_expression()
                        return Binding(name, value)
                    else:
                        return Binding(name, None)
                elif next_t.type == "OPERATOR" and next_t.value == "<:":
                    self.advance()
                    self.advance()
                    value = self.parse_value_expression()
                    return ("rebind", name, value)
                elif next_t.type == "OPERATOR" and next_t.value == ":>":
                    self.advance()
                    self.advance()
                    value = self.parse_value_expression()
                    return BindOrRebind(name, value)
        expr1 = self.parse_value_expression()
        if self.peek() and self.peek().type == "OPERATOR" and self.peek().value == ":>":
            self.advance()
            expr2 = self.parse_value_expression()
            if isinstance(expr1, VarInvoke) and isinstance(expr2, VarInvoke):
                raise EnzoParseError("Ambiguous :> binding: both sides are variables")
            elif isinstance(expr1, VarInvoke):
                return BindOrRebind(expr1.name, expr2)
            elif isinstance(expr2, VarInvoke):
                return BindOrRebind(expr2.name, expr1)
            else:
                raise EnzoParseError(":> must have a variable on one side")
        return expr1

    def parse_statements(self):
        stmts = []
        while self.pos < len(self.tokens):
            stmts.append(self.parse_statement())
            if self.peek() and self.peek().type == "OPERATOR" and self.peek().value in (";",):
                self.advance()
            else:
                break
        return stmts

    def parse_block(self):
        stmts = self.parse_statements()
        if len(stmts) == 1:
            return stmts[0]
        else:
            return stmts

    def parse(self):
        ast = self.parse_block()
        if self.pos != len(self.tokens):
            raise EnzoParseError(error_message_unexpected_token(self.tokens[self.pos]))
        return ast

    def parse_program(self):
        statements = []
        while self.pos < len(self.tokens):
            stmt = self.parse_statement()
            statements.append(stmt)
            if self.peek() and self.peek().type == "OPERATOR" and self.peek().value in (";", ","):
                self.advance()
        return Program(statements)

# Top-level API for main interpreter and debug module

def parse(src):
    parser = Parser(src)
    return parser.parse()

def parse_program(src):
    parser = Parser(src)
    return parser.parse_program()

# TODO: Implement parse_statement, parse_expr, parse_function_atom, etc.
# Each should take a context argument (e.g., 'top-level', 'binding', 'expression')
