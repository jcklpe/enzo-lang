# Main parser entry point for Enzo

from .ast_nodes import *
from .tokenizer import Tokenizer
from src.error_handling import EnzoParseError
from src.error_messaging import (
    error_message_expected_type,
    error_message_unexpected_token,
    error_message_unmatched_parenthesis,
    error_message_unmatched_bracket,
    error_message_unmatched_brace,
    # ...other error messages as needed...
)
from .parser_utilities import get_code_line, peek, advance, expect

# Import parsing helpers from submodules
from .parser_function import parse_function_atom
from .parser_table import parse_table_atom
from .parser_list import parse_list_atom

class Parser:
    def __init__(self, src):
        self.src = src
        self.src_lines = src.splitlines()
        self.tokens = Tokenizer(src).tokenize()
        self.tokens = [t for t in self.tokens if t.type not in ("NEWLINE", "COMMENT", "SKIP")]
        self.pos = 0

    def _get_code_line(self, token):
        return get_code_line(self.src_lines, token, self.src)

    def peek(self):
        return peek(self.tokens, self.pos)

    def advance(self):
        token, self.pos = advance(self.tokens, self.pos)
        return token

    def expect(self, type_):
        return expect(self, type_)

    def parse_function_atom(self):
        # Delegate to parser_function.py
        return parse_function_atom(self)

    def parse_list_atom(self):
        # Delegate to parser_list.py
        return parse_list_atom(self)

    def parse_table_atom(self):
        # Delegate to parser_table.py
        return parse_table_atom(self)

    def parse_postfix(self, base):
        # Correctly handle chained dot-number and dot-variable for nested indexing
        debug_chain = []  # DEBUG: collect chain for print
        while self.peek() and self.peek().type == "DOT":
            self.advance()  # consume DOT
            t = self.peek()
            code_line = self._get_code_line(t) if t else None
            if t and t.type == "NUMBER_TOKEN":
                num_token = self.advance().value
                # Use int if possible, else float
                if '.' in num_token:
                    num = float(num_token)
                else:
                    num = int(num_token)
                debug_chain.append(f".{{{num}}}")  # DEBUG
                base = ListIndex(base, NumberAtom(num, code_line=code_line), code_line=code_line)
            elif t and t.type == "KEYNAME":
                key = self.advance().value
                if key.startswith("$"):
                    debug_chain.append(f".${{key}}")  # DEBUG
                    base = ListIndex(base, VarInvoke(key, code_line=code_line), code_line=code_line)
                else:
                    debug_chain.append(f".{key}")  # DEBUG
                    base = TableIndex(base, key, code_line=code_line)
            elif t and t.type == "TEXT_TOKEN":
                # Allow string as index: $list."foo"
                text_val = self.advance().value[1:-1]
                debug_chain.append(f'."{text_val}"')  # DEBUG
                base = ListIndex(base, TextAtom(text_val, code_line=code_line), code_line=code_line)
            else:
                # If not a valid index or property, break
                break
        # DEBUG: print the final AST for chained dot access
        if debug_chain:
            pass  # print(f"[DEBUG parser] parse_postfix chain: {debug_chain} -> AST: {base}")
        return base

    def parse_atom(self):
        t = self.peek()
        if not t:
            raise EnzoParseError(error_message_unexpected_token(t), code_line=self._get_code_line(t))
        code_line = self._get_code_line(t)
        if t.type == "NUMBER_TOKEN":
            val = self.advance().value
            if '.' in val:
                node = NumberAtom(float(val), code_line=code_line)
            else:
                node = NumberAtom(int(val), code_line=code_line)
        elif t.type == "TEXT_TOKEN":
            node = TextAtom(self.advance().value[1:-1], code_line=code_line)
        elif t.type == "KEYNAME":
            node = VarInvoke(self.advance().value, code_line=code_line)
        elif t.type == "AT":
            self.advance()
            t2 = self.expect("KEYNAME")
            code_line2 = self._get_code_line(t2)
            node = FunctionRef(t2.value, code_line=code_line2)
        elif t.type == "LPAR":
            node = self.parse_function_atom()
            # --- FIX: Consume trailing semicolon/comma after function atom ---
            while self.peek() and self.peek().type in ("SEMICOLON", "COMMA"):
                self.advance()
        elif t.type == "LBRACK":
            node = self.parse_list_atom()
        elif t.type == "LBRACE":
            node = self.parse_table_atom()
        elif t.type == "MINUS":
            self.advance()
            t2 = self.peek()
            from src.error_messaging import error_message_double_minus
            if t2 and t2.type == "MINUS":
                raise EnzoParseError(error_message_double_minus(t2), code_line=self._get_code_line(t2))
            if t2 and t2.type == "NUMBER_TOKEN" and t2.value.startswith('-'):
                raise EnzoParseError(error_message_double_minus(t2), code_line=self._get_code_line(t2))
            if t2 and t2.type == "NUMBER_TOKEN":
                self.advance()
                val = t2.value
                if '.' in val:
                    node = NumberAtom(float('-' + val.lstrip('-')), code_line=code_line)
                else:
                    node = NumberAtom(int('-' + val.lstrip('-')), code_line=code_line)
            else:
                raise EnzoParseError(error_message_unexpected_token(t2), code_line=self._get_code_line(t2))
        else:
            raise EnzoParseError(error_message_unexpected_token(t), code_line=self._get_code_line(t))
        # Always parse postfix after atom (to allow nested function atoms, chained indices, etc.)
        return self.parse_postfix(node)

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
        code_line = self._get_code_line(t) if t else None
        if t and t.type == "SEMICOLON":
            err = EnzoParseError(error_message_unexpected_token(t))
            err.line = getattr(t, "line", 1)
            err.column = getattr(t, "column", 1)
            err.code_line = code_line
            raise err

        # Support assignment to variable, list index, or table index
        # Parse a value expression (could be VarInvoke, ListIndex, TableIndex, etc.)
        expr1 = self.parse_value_expression()
        # Assignment: <:
        if self.peek() and self.peek().type == "REBIND_LEFTWARD":
            self.advance()  # consume REBIND_LEFTWARD
            value = self.parse_value_expression()
            return BindOrRebind(expr1, value, code_line=code_line)
        # Variable binding: $x: ...
        if isinstance(expr1, VarInvoke) and self.peek() and self.peek().type == "BIND":
            self.advance()  # consume BIND
            # Support empty bind: $x: ;
            if self.peek() and self.peek().type == "SEMICOLON":
                return Binding(expr1.name, None, code_line=code_line)
            value = self.parse_value_expression()
            return Binding(expr1.name, value, code_line=code_line)
        # Implicit bind-or-rebind: :>
        if self.peek() and self.peek().type == "REBIND_RIGHTWARD":
            self.advance()
            expr2 = self.parse_value_expression()
            if isinstance(expr1, VarInvoke) and isinstance(expr2, VarInvoke):
                raise EnzoParseError("Ambiguous :> binding: both sides are variables", code_line=code_line)
            elif isinstance(expr1, VarInvoke):
                return BindOrRebind(expr1.name, expr2, code_line=code_line)
            elif isinstance(expr2, VarInvoke):
                return BindOrRebind(expr2.name, expr1, code_line=code_line)
            else:
                raise EnzoParseError(":> must have a variable on one side", code_line=code_line)
        return expr1

    def parse_statements(self):
        stmts = []
        while self.pos < len(self.tokens):
            stmt = self.parse_statement()
            stmts.append(stmt)
            # Accept and consume all consecutive semicolons or commas after a statement
            while self.peek() and self.peek().type in ("SEMICOLON", "COMMA"):
                self.advance()
            # Stop if next token is a closing delimiter or end of input
            if self.peek() and self.peek().type in ("RPAR", "RBRACK", "RBRACE"):
                break
            elif not self.peek():
                break
            # Otherwise, continue parsing next statement
        return stmts

    def parse_block(self):
        stmts = self.parse_statements()
        # Always return the list of statements, even if length 1
        return stmts

    def parse(self):
        ast = self.parse_block()
        # Consume any trailing semicolons/commas after a block
        while self.peek() and self.peek().type in ("SEMICOLON", "COMMA"):
            self.advance()
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
    #Parse a single Enzo source string into an AST (single statement/block).
    parser = Parser(src)
    return parser.parse()

def parse_program(src):
    #Parse a full Enzo source string into a Program AST (multiple statements).
    parser = Parser(src)
    return parser.parse_program()
    parser = Parser(src)
    return parser.parse_program()
    return parser.parse_program()
    parser = Parser(src)
    return parser.parse_program()
