# Recursive-descent parser skeleton for Enzo
# This is a scaffold for a context-aware parser

from .ast_nodes import *
from .tokenizer import Tokenizer
from src.error_handling import EnzoParseError
from src.error_messaging import (
    error_message_expected_type,
    error_message_unexpected_token,
    error_message_double_minus,
    error_message_unmatched_bracket,
    error_message_unmatched_parenthesis,
    error_message_unmatched_brace,
    error_message_double_comma,
    error_message_empty_list_comma,
    error_message_excess_leading_comma,
    error_message_double_comma_table,
    error_message_leading_comma_table,
    error_message_empty_table_comma,
    # ...other error messages as needed...
)

class Parser:
    def __init__(self, src):
        self.src = src
        self.src_lines = src.splitlines()
        self.tokens = Tokenizer(src).tokenize()
        self.tokens = [t for t in self.tokens if t.type not in ("NEWLINE", "COMMENT", "SKIP")]
        self.pos = 0

    def _get_code_line(self, token):
        if hasattr(token, 'line') and token.line is not None:
            line_num = token.line
            if 1 <= line_num <= len(self.src_lines):
                return self.src_lines[line_num - 1]
        return self.src_lines[0] if self.src_lines else self.src

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def advance(self):
        self.pos += 1
        return self.tokens[self.pos-1]

    def expect(self, type_):
        t = self.peek()
        if not t or t.type != type_:
            prev = self.tokens[self.pos - 1] if self.pos > 0 else None
            line = getattr(prev, "line", 1) if prev else 1
            column = getattr(prev, "end", 0) + 1 if prev else 1
            if type_ == "RPAR":
                raise EnzoParseError(error_message_unmatched_parenthesis(), line=line, column=column, code_line=self._get_code_line(prev))
            elif type_ == "RBRACK":
                raise EnzoParseError(error_message_unmatched_bracket(), line=line, column=column, code_line=self._get_code_line(prev))
            elif type_ == "RBRACE":
                raise EnzoParseError(error_message_unmatched_brace(), line=line, column=column, code_line=self._get_code_line(prev))
            else:
                raise EnzoParseError(error_message_expected_type(type_, t), line=line, column=column, code_line=self._get_code_line(prev))
        return self.advance()

    def parse_function_atom(self):
        self.expect("LPAR")  # '('
        # --- FIX: Allow empty function atom ---
        t = self.peek()
        if t and t.type == "RPAR":
            self.advance()
            return FunctionAtom([], [], [], code_line=self._get_code_line(t))
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
        saw_item = False
        t_start = self.peek()
        code_line = self._get_code_line(t_start) if t_start else None
        while True:
            t = self.peek()
            if t and t.type == "RBRACK":
                self.advance()
                break
            if t and t.type == "COMMA":
                t2 = self.tokens[self.pos + 1] if self.pos + 1 < len(self.tokens) else None
                if t2 and t2.type == "RBRACK" and not saw_item:
                    raise EnzoParseError(error_message_empty_list_comma(), code_line=self._get_code_line(t))
                if not saw_item:
                    raise EnzoParseError(error_message_excess_leading_comma(), code_line=self._get_code_line(t))
                raise EnzoParseError(error_message_double_comma(), code_line=self._get_code_line(t))
            if t is None:
                raise EnzoParseError(error_message_unmatched_bracket(), code_line=None)
            if t.type == "SEMICOLON":
                raise EnzoParseError(error_message_unmatched_bracket(), code_line=self._get_code_line(t))
            elements.append(self.parse_value_expression())
            saw_item = True
            t = self.peek()
            if t and t.type == "COMMA":
                self.advance()
                t2 = self.peek()
                if t2 and t2.type == "RBRACK":
                    self.advance()
                    break
                if t2 and t2.type == "COMMA":
                    raise EnzoParseError(error_message_double_comma(), code_line=self._get_code_line(t2))
            elif t and t.type == "RBRACK":
                self.advance()
                break
            elif t:
                raise EnzoParseError(error_message_unmatched_bracket(), code_line=self._get_code_line(t))
            else:
                raise EnzoParseError(error_message_unmatched_bracket(), code_line=None)
        return ListAtom(elements, code_line=code_line)

    def parse_table_atom(self):
        self.expect("LBRACE")
        items = []
        trailing_comma = False
        t_start = self.peek()
        code_line = self._get_code_line(t_start) if t_start else None
        if self.peek() and not (self.peek().type == "RBRACE"):
            key_value_pairs = []
            saw_item = False
            while True:
                t = self.peek()
                if t is None:
                    raise EnzoParseError(error_message_unmatched_brace(), code_line=self._get_code_line(t))
                if t.type == "RBRACE":
                    if not saw_item and trailing_comma:
                        raise EnzoParseError(error_message_empty_table_comma(), code_line=self._get_code_line(t))
                    break
                if t.type == "COMMA":
                    t2 = self.tokens[self.pos + 1] if self.pos + 1 < len(self.tokens) else None
                    # --- FIX: distinguish empty table with comma ---
                    if not saw_item:
                        if t2 and t2.type == "RBRACE":
                            raise EnzoParseError(error_message_empty_table_comma(), code_line=self._get_code_line(t))
                        else:
                            raise EnzoParseError(error_message_leading_comma_table(), code_line=self._get_code_line(t))
                    if t2 and t2.type == "COMMA":
                        raise EnzoParseError(error_message_double_comma_table(), code_line=self._get_code_line(t2))
                    self.advance()
                    trailing_comma = True
                    continue
                if t.type != "KEYNAME":
                    raise EnzoParseError(error_message_unmatched_brace(), code_line=self._get_code_line(t))
                key = self.expect("KEYNAME").value
                self.expect("COLON")
                value = self.parse_value_expression()
                key_value_pairs.append((key, value))
                saw_item = True
                t = self.peek()
                if t and t.type == "COMMA":
                    self.advance()
                    trailing_comma = True
                    # Check for double comma
                    t2 = self.peek()
                    if t2 and t2.type == "COMMA":
                        raise EnzoParseError(error_message_double_comma_table(), code_line=self._get_code_line(t2))
                else:
                    trailing_comma = False
            # Overwrite duplicate keys: last one wins, preserve order of last occurrence
            seen = {}
            ordered = []
            for k, v in key_value_pairs:
                if k in seen:
                    # Remove previous occurrence
                    ordered = [pair for pair in ordered if pair[0] != k]
                seen[k] = v
                ordered.append((k, v))
            items = ordered
        t = self.peek()
        if not t or t.type != "RBRACE":
            raise EnzoParseError(error_message_unmatched_brace(), code_line=self._get_code_line(t))
        self.advance()
        return TableAtom(items, code_line=code_line)

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
                return NumberAtom(float(val), code_line=code_line)
            else:
                return NumberAtom(int(val), code_line=code_line)
        elif t.type == "TEXT_TOKEN":
            return TextAtom(self.advance().value[1:-1], code_line=code_line)
        elif t.type == "KEYNAME":
            return VarInvoke(self.advance().value, code_line=code_line)
        elif t.type == "AT":
            self.advance()
            t2 = self.expect("KEYNAME")
            code_line2 = self._get_code_line(t2)
            return FunctionRef(t2.value, code_line=code_line2)
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
                raise EnzoParseError(error_message_double_minus(t2), code_line=self._get_code_line(t2))
            if t2 and t2.type == "NUMBER_TOKEN" and t2.value.startswith('-'):
                raise EnzoParseError(error_message_double_minus(t2), code_line=self._get_code_line(t2))
            if t2 and t2.type == "NUMBER_TOKEN":
                self.advance()
                val = t2.value
                if '.' in val:
                    return NumberAtom(float('-' + val.lstrip('-')), code_line=code_line)
                else:
                    return NumberAtom(int('-' + val.lstrip('-')), code_line=code_line)
            else:
                raise EnzoParseError(error_message_unexpected_token(t2), code_line=self._get_code_line(t2))
        else:
            raise EnzoParseError(error_message_unexpected_token(t), code_line=self._get_code_line(t))

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
        if isinstance(expr1, VarInvoke) and self.peek() and self.peek().type == "COLON":
            self.advance()  # consume COLON
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
# TODO: Implement parse_statement, parse_expr, parse_function_atom, etc.
# Each should take a context argument (e.g., 'top-level', 'binding', 'expression')
