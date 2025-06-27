# Recursive-descent parser skeleton for Enzo
# This is a scaffold for a context-aware parser

from .ast_nodes import *
from .tokenizer import Tokenizer
from src.error_handling import EnzoParseError
from src.error_messaging import error_message_expected_type, error_message_unexpected_token, error_message_double_minus

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
        self.expect("LPAR")  # '('
        # Look ahead: function definition or value expression?
        t = self.peek()
        if t and t.type == "KEYNAME":
            # Look ahead for KEYNAME : (function param or local var)
            save_pos = self.pos
            name = t.value
            self.advance()
            if self.peek() and self.peek().type == "COLON":
                # Function definition or local var
                self.pos = save_pos  # rewind
                items = []
                sep_seen = False
                while self.peek() and not (self.peek().type == "RPAR"):
                    t = self.peek()
                    if t.type == "KEYNAME":
                        name = self.advance().value
                        if self.peek() and self.peek().type == "COLON":
                            self.advance()
                            if self.peek() and not (self.peek().type in ("COMMA", "SEMICOLON", "RPAR")):
                                value_expression = self.parse_value_expression()
                                items.append(Binding(name, value_expression))
                            else:
                                items.append(Binding(name, None))
                        else:
                            items.append(name)
                    else:
                        items.append(self.parse_value_expression())
                    if self.peek() and self.peek().type in ("COMMA", "SEMICOLON"):
                        sep_seen = True
                        self.advance()
                self.expect("RPAR")
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
        self.expect("RPAR")
        return FunctionAtom([], [], [expr])

    def parse_list_atom(self):
        self.expect("LBRACK")
        elements = []
        trailing_comma = False
        if self.peek() and not (self.peek().type == "RBRACK"):
            while True:
                elements.append(self.parse_value_expression())
                if self.peek() and self.peek().type == "COMMA":
                    self.advance()
                    trailing_comma = True
                else:
                    trailing_comma = False
                    break
        self.expect("RBRACK")
        return ListAtom(elements)

    def parse_table_atom(self):
        self.expect("LBRACE")
        items = []
        trailing_comma = False
        if self.peek() and not (self.peek().type == "RBRACE"):
            while True:
                key = self.expect("KEYNAME").value
                self.expect("COLON")
                value = self.parse_value_expression()
                items.append((key, value))
                if self.peek() and self.peek().type == "COMMA":
                    self.advance()
                    trailing_comma = True
                else:
                    trailing_comma = False
                    break
        self.expect("RBRACE")
        return TableAtom(items)

    def parse_postfix(self, base):
        # Use DOT token for property/index access
        while self.peek() and self.peek().type == "DOT":
            self.advance()
            t = self.peek()
            if t and t.type == "NUMBER_TOKEN":
                num_token = self.advance().value
                # Use int if possible, else float
                if '.' in num_token:
                    num = float(num_token)
                else:
                    num = int(num_token)
                base = ListIndex(base, NumberAtom(num))
            elif t and t.type == "KEYNAME":
                key = self.advance().value
                if key.startswith("$"):
                    # Variable index: ListIndex(base, VarInvoke(key))
                    base = ListIndex(base, VarInvoke(key))
                else:
                    # Property access: TableIndex(base, key)
                    base = TableIndex(base, key)
            else:
                break
        return base

    def parse_atom(self):
        t = self.peek()
        if not t:
            raise EnzoParseError("Unexpected end of input")
        if t.type == "NUMBER_TOKEN":
            val = self.advance().value
            if '.' in val:
                return NumberAtom(float(val))
            else:
                return NumberAtom(int(val))
        elif t.type == "TEXT_TOKEN":
            return TextAtom(self.advance().value[1:-1])
        elif t.type == "KEYNAME":
            return VarInvoke(self.advance().value)
        elif t.type == "AT":
            self.advance()
            t2 = self.expect("KEYNAME")
            return FunctionRef(t2.value)
        elif t.type == "LPAR":
            return self.parse_function_atom()
        elif t.type == "LBRACK":
            return self.parse_list_atom()
        elif t.type == "LBRACE":
            return self.parse_table_atom()
        elif t.type == "MINUS":
            self.advance()
            t2 = self.peek()
            from src.error_messaging import error_message_double_minus
            if t2 and t2.type == "MINUS":
                raise EnzoParseError(error_message_double_minus(t2))
            if t2 and t2.type == "NUMBER_TOKEN" and t2.value.startswith('-'):
                raise EnzoParseError(error_message_double_minus(t2))
            if t2 and t2.type == "NUMBER_TOKEN":
                self.advance()
                val = t2.value
                if '.' in val:
                    return NumberAtom(float('-' + val.lstrip('-')))
                else:
                    return NumberAtom(int('-' + val.lstrip('-')))
            else:
                raise EnzoParseError(error_message_unexpected_token(t2))
        else:
            raise EnzoParseError(error_message_unexpected_token(t))

    def parse_factor(self):
        node = self.parse_atom()
        node = self.parse_postfix(node)
        while self.peek() and self.peek().type in ("STAR", "SLASH"):
            op = self.advance()
            right = self.parse_atom()
            if op.type == "STAR":
                node = MulNode(node, right)
            else:
                node = DivNode(node, right)
        return node

    def parse_term(self):
        node = self.parse_factor()
        while self.peek() and self.peek().type in ("PLUS", "MINUS"):
            op = self.advance()
            right = self.parse_factor()
            if op.type == "PLUS":
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
            # Check for rebinding: $x <: expr
            if self.pos + 1 < len(self.tokens):
                next_tok = self.tokens[self.pos + 1]
                if next_tok.type == "LT_COLON":
                    self.advance()  # KEYNAME
                    self.advance()  # LT_COLON
                    value = self.parse_value_expression()
                    return BindOrRebind(name, value)
                elif next_tok.type == "COLON":
                    self.advance()  # KEYNAME
                    self.advance()  # COLON
                    # Support empty bind: $x: ;
                    if self.peek() and self.peek().type == "SEMICOLON":
                        return Binding(name, None)
                    value = self.parse_value_expression()
                    return Binding(name, value)
        expr1 = self.parse_value_expression()
        if self.peek() and self.peek().type == "COLON_GT":
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
            if self.peek() and self.peek().type in ("SEMICOLON",):
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
            if self.peek() and self.peek().type in ("SEMICOLON", "COMMA"):
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
