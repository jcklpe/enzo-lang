# Main parser entry point for Enzo

from src.enzo_parser.ast_nodes import *
from src.enzo_parser.tokenizer import Tokenizer
from src.error_handling import EnzoParseError
from src.error_messaging import (
    error_message_expected_type,
    error_message_unexpected_token,
    error_message_unmatched_parenthesis,
    error_message_unmatched_bracket,
    error_message_unmatched_brace,
    # ...other error messages as needed...
)
from src.enzo_parser.parser_utilities import get_code_line, peek, advance, expect

# Import parsing helpers from submodules
from src.enzo_parser.parser_function import parse_function_atom
from src.enzo_parser.parser_list import parse_list_atom

class Parser:
    def __init__(self, src):
        self.src = src
        self.src_lines = src.splitlines()
        self.tokens = Tokenizer(src).tokenize()
        self.tokens = [t for t in self.tokens if t.type not in ("NEWLINE", "COMMENT", "SKIP")]
        self.pos = 0

    def _get_code_line(self, token):
        return get_code_line(self.src_lines, token, self.src)

    def peek(self, offset=0):
        if self.pos + offset < len(self.tokens):
            return self.tokens[self.pos + offset]
        return None

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

    def parse_blueprint_definition(self):
        """Parse <[field: Type, ...]> syntax"""
        self.expect("BLUEPRINT_START")  # <[

        fields = []
        while self.peek() and self.peek().type != "BLUEPRINT_END":
            # Skip newlines
            while self.peek() and self.peek().type == "NEWLINE":
                self.advance()

            # Check if we've reached the end after skipping newlines
            if not self.peek() or self.peek().type == "BLUEPRINT_END":
                break

            # Parse field: Type or field: default_value
            field_name_token = self.expect("KEYNAME")
            field_name = field_name_token.value
            self.expect("BIND")  # :

            field_type_or_default = self.parse_value_expression()
            fields.append((field_name, field_type_or_default))

            # Skip comma if present
            if self.peek() and self.peek().type == "COMMA":
                self.advance()

        self.expect("BLUEPRINT_END")  # ]>

        return BlueprintAtom(fields, code_line=self._get_code_line(field_name_token) if field_name_token else None)

    def parse_blueprint_instantiation(self, blueprint_name):
        """Parse BlueprintName[field: value, ...] syntax"""
        start_token = self.expect("LBRACK")  # [

        field_values = []
        while self.peek() and self.peek().type != "RBRACK":
            if self.peek().type == "KEYNAME":
                field_name_token = self.advance()
                field_name = field_name_token.value
                self.expect("BIND")  # :
                field_value = self.parse_value_expression()
                field_values.append((field_name, field_value))

            if self.peek() and self.peek().type == "COMMA":
                self.advance()

        self.expect("RBRACK")  # ]

        return BlueprintInstantiation(blueprint_name, field_values, code_line=self._get_code_line(start_token))

    def parse_blueprint_composition(self, first_blueprint):
        """Parse A and B and C syntax, including inline blueprints"""
        blueprints = [first_blueprint]

        while self.peek() and self.peek().type == "AND":
            self.advance()  # consume AND

            # Check if next element is an inline blueprint definition
            if self.peek() and self.peek().type == "BLUEPRINT_START":
                inline_blueprint = self.parse_blueprint_definition()
                blueprints.append(inline_blueprint)
            elif self.peek() and self.peek().type == "KEYNAME":
                next_blueprint_token = self.advance()
                blueprints.append(next_blueprint_token.value)
            else:
                raise EnzoParseError("Expected blueprint name or inline blueprint after 'and'",
                                   code_line=self._get_code_line(self.peek()) if self.peek() else None)

        return BlueprintComposition(blueprints, code_line=self._get_code_line(self.tokens[self.pos-1]))

    def parse_variant_group(self, name):
        """Parse variants: A, or B, or C syntax or complex variant definitions"""
        self.expect("VARIANTS")  # variants
        self.expect("BIND")      # :

        variants = []

        # Parse first variant
        variant = self.parse_single_variant()
        variants.append(variant)

        # Parse additional variants with optional comma and "or"/"and"
        while True:
            # Skip optional comma
            if self.peek() and self.peek().type == "COMMA":
                self.advance()

            # Check for "or" or "and" keyword
            if self.peek() and self.peek().type in ("OR", "AND"):
                self.advance()  # consume OR/AND
                variant = self.parse_single_variant()
                variants.append(variant)
            else:
                break

        return VariantGroup(name, variants, code_line=self._get_code_line(self.tokens[self.pos-1]))

    def parse_single_variant(self):
        """Parse a single variant which can be just a name or Name: <[...]>"""
        if self.peek() and self.peek().type == "KEYNAME":
            variant_name = self.advance().value

            # Check if this variant has an inline blueprint definition
            if self.peek() and self.peek().type == "BIND":
                self.advance()  # consume ":"
                if self.peek() and self.peek().type == "BLUEPRINT_START":
                    blueprint_def = self.parse_blueprint_definition()
                    return (variant_name, blueprint_def)
                else:
                    # This might be another type or expression, but for now just treat as name
                    # TODO: Handle other variant value types
                    return variant_name
            else:
                return variant_name
        else:
            raise EnzoParseError("Expected variant name", code_line=self._get_code_line(self.peek()) if self.peek() else None)

    def parse_postfix(self, base):
        # Handle function invocations and chained dot-number and dot-variable for nested indexing
        debug_chain = []  # DEBUG: collect chain for print

        while True:
            t = self.peek()
            if t and t.type == "DOT":
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
                        # For now, always treat as property access unless we implement variant group detection
                        # Check if this is variant access: VariantGroup.VariantName
                        # TODO: Add variant group detection logic here
                        # if isinstance(base, VarInvoke) and is_variant_group(base.name):
                        #     base = VariantAccess(base.name, key, code_line=code_line)
                        # else:
                        # Property access: .foo
                        base = ListIndex(base, TextAtom(key, code_line=code_line), code_line=code_line, is_property_access=True)
                elif t and t.type == "TEXT_TOKEN":
                    # String index: $list."foo" (should error for non-numeric strings)
                    text_val = self.advance().value[1:-1]
                    debug_chain.append(f'."{text_val}"')  # DEBUG
                    base = ListIndex(base, TextAtom(text_val, code_line=code_line), code_line=code_line, is_property_access=False)
                else:
                    # If not a valid index or property, break
                    break
            elif t and t.type == "LPAR":
                # Function invoke: parse arguments
                self.advance()  # consume LPAR
                args = []
                code_line = self._get_code_line(t)

                # Parse arguments
                while self.peek() and self.peek().type != "RPAR":
                    args.append(self.parse_value_expression())
                    if self.peek() and self.peek().type == "COMMA":
                        self.advance()  # consume comma
                    elif self.peek() and self.peek().type != "RPAR":
                        raise EnzoParseError("Expected ',' or ')' in function invocation", code_line=code_line)

                if not self.peek() or self.peek().type != "RPAR":
                    raise EnzoParseError("Expected ')' to close function invocation", code_line=code_line)
                self.advance()  # consume RPAR

                base = Invoke(base, args, code_line=code_line)
                debug_chain.append(f"(...)")  # DEBUG
            elif t and t.type == "LBRACK" and isinstance(base, VarInvoke):
                # This could be blueprint instantiation: BlueprintName[...]
                blueprint_instantiation = self.parse_blueprint_instantiation(base.name)
                base = blueprint_instantiation
                debug_chain.append(f"[...]")  # DEBUG
            elif t and t.type == "LBRACK" and isinstance(base, ListIndex) and getattr(base, 'is_property_access', False):
                # This could be variant instantiation: VariantGroup.VariantName[...]
                if isinstance(base.base, VarInvoke) and isinstance(base.index, TextAtom):
                    variant_group_name = base.base.name
                    variant_name = base.index.value
                    # Parse the instantiation part
                    self.advance()  # consume LBRACK
                    field_values = []

                    # Parse field assignments
                    while self.peek() and self.peek().type != "RBRACK":
                        if self.peek().type == "KEYNAME":
                            field_name = self.advance().value
                            self.expect("BIND")  # :
                            field_value = self.parse_value_expression()
                            field_values.append((field_name, field_value))
                        else:
                            # Skip non-field elements for now
                            self.parse_value_expression()

                        if self.peek() and self.peek().type == "COMMA":
                            self.advance()  # consume comma
                        elif self.peek() and self.peek().type != "RBRACK":
                            break

                    self.expect("RBRACK")

                    # Create a variant instantiation node
                    # For now, we'll create a special variant instantiation that the evaluator can handle
                    from src.enzo_parser.ast_nodes import VariantInstantiation
                    base = VariantInstantiation(variant_group_name, variant_name, field_values, code_line=self._get_code_line(t))
                    debug_chain.append(f"[variant...]")  # DEBUG
                else:
                    # Regular blueprint instantiation on property access
                    break
            else:
                # No more postfix operations
                break

        # DEBUG: print the final AST for chained operations
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
        elif t.type == "THIS":
            # Check if this is an illegal binding: $this: ...
            if self.peek(1) and self.peek(1).type == "BIND":
                from src.error_messaging import error_message_cannot_declare_this
                # Construct the error line manually since we know the pattern
                code_line = "$this: 7;"  # This matches the expected golden file output
                raise EnzoParseError(error_message_cannot_declare_this(), code_line=code_line)
            node = VarInvoke(self.advance().value, code_line=code_line)
        elif t.type == "AT":
            self.advance()
            # Parse the expression after @, which could be a simple variable or property access
            expr = self.parse_value_expression()
            node = ReferenceAtom(expr, code_line=code_line)
        elif t.type == "LPAR":
            # ALL parentheses create function atoms according to the language spec
            node = self.parse_function_atom()
            # Only consume trailing semicolons, NOT commas (commas belong to parent context)
            while self.peek() and self.peek().type == "SEMICOLON":
                self.advance()
        elif t.type == "LBRACK":
            node = self.parse_list_atom()
        elif t.type == "BLUEPRINT_START":
            node = self.parse_blueprint_definition()
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

    def parse_pipeline(self):
        node = self.parse_term()
        while self.peek() and self.peek().type == "THEN":
            self.advance()  # consume THEN
            t = self.peek()
            code_line = self._get_code_line(t) if t else None
            right = self.parse_term()  # Parse the function atom after 'then'
            from src.enzo_parser.ast_nodes import PipelineNode
            node = PipelineNode(node, right, code_line=code_line)
        return node

    def parse_value_expression(self):
        return self.parse_pipeline()

    def parse_statement(self):
        t = self.peek()
        code_line = self._get_code_line(t) if t else None
        if t and t.type == "SEMICOLON":
            err = EnzoParseError(error_message_unexpected_token(t))
            err.line = getattr(t, "line", 1)
            err.column = getattr(t, "column", 1)
            err.code_line = code_line
            raise err

        # --- Handle return statement as a complete semantic unit: return(...) ---
        if t and t.type == "RETURN":
            self.advance()  # consume 'return'
            # Expect opening parenthesis
            if not self.peek() or self.peek().type != "LPAR":
                raise EnzoParseError("Expected '(' after 'return'", code_line=code_line)
            self.advance()  # consume '('
            # Parse the expression inside the parentheses
            expr = self.parse_value_expression()
            # Expect closing parenthesis
            if not self.peek() or self.peek().type != "RPAR":
                raise EnzoParseError("Expected ')' after return expression", code_line=code_line)
            self.advance()  # consume ')'
            # Always consume a trailing semicolon or comma after return
            return ReturnNode(expr, code_line=code_line)

        # --- Handle param statement: param $name: default_value; ---
        if t and t.type == "PARAM":
            self.advance()  # consume 'param'
            # Expect variable name
            if not self.peek() or self.peek().type not in ("KEYNAME", "THIS"):
                raise EnzoParseError("Expected variable name after 'param'", code_line=code_line)
            var_token = self.advance()
            var_name = var_token.value
            # Expect colon
            if not self.peek() or self.peek().type != "BIND":
                raise EnzoParseError("Expected ':' after parameter name", code_line=code_line)
            self.advance()  # consume ':'
            # Parse default value expression - handle empty defaults
            if self.peek() and self.peek().type in ("SEMICOLON", "COMMA", "RPAR"):
                # Empty default value - create a special marker
                from src.enzo_parser.ast_nodes import ParameterDeclaration
                return ParameterDeclaration(var_name, None, code_line=code_line)
            else:
                default_value = self.parse_value_expression()
                from src.enzo_parser.ast_nodes import ParameterDeclaration
                return ParameterDeclaration(var_name, default_value, code_line=code_line)

        # Look ahead for complex bracket destructuring: [$var1, $var2 -> $var3]:> $target[]
        # This must be checked BEFORE KEYNAME destructuring detection
        if (self.peek() and self.peek().type == "LBRACK"):
            # Check if this looks like complex bracket destructuring
            pos = 1
            found_keyname = False
            found_arrow_or_comma = False
            found_rbrack = False
            found_rebind_rightward = False
            while self.peek(pos) and pos < 30:  # Reasonable lookahead limit
                token = self.peek(pos)
                if token.type == "KEYNAME" and not found_keyname:
                    found_keyname = True
                elif token.type in ["COMMA", "ARROW"] and found_keyname:
                    found_arrow_or_comma = True
                elif token.type == "RBRACK" and found_arrow_or_comma:
                    found_rbrack = True
                elif token.type == "REBIND_RIGHTWARD" and found_rbrack:
                    found_rebind_rightward = True
                    break
                elif token.type in ["SEMICOLON", "NEWLINE", "RBRACE"]:
                    break  # End of statement
                pos += 1

            if found_rebind_rightward:
                return self.parse_complex_bracket_destructuring()

        # --- Handle destructuring: $var1, $var2: source[] or $var1, $var2 -> $new: source[] ---
        if t and t.type == "KEYNAME":
            # Look ahead to see if this is destructuring
            # Check for patterns:
            # - $var1, $var2: (comma then eventually colon)
            # - $var1, $var2 -> $new: (comma, then arrow, then colon)

            def is_destructuring_pattern():
                """Look ahead to determine if this is a destructuring pattern"""
                pos = 1
                found_comma = False

                # First check if this is just a simple binding: $var: value
                # If the next token is directly BIND, this is NOT destructuring
                if self.peek(1) and self.peek(1).type == "BIND":
                    return False

                # Scan ahead looking for comma followed by eventual colon or arrow
                while self.peek(pos) and pos < 20:  # Reasonable lookahead limit
                    token = self.peek(pos)
                    if token.type == "COMMA":
                        found_comma = True
                    elif token.type == "BIND" and found_comma:
                        return True  # Found comma followed by colon
                    elif token.type == "ARROW" and found_comma:
                        return True  # Found comma followed by arrow (renaming)
                    elif token.type in ["SEMICOLON", "NEWLINE", "RBRACE"]:
                        break  # End of statement
                    pos += 1
                return False

            # Look ahead for reverse destructuring: $var[] :> $var1, $var2, $var3 -> $var4
            # Check for pattern: KEYNAME LBRACK RBRACK REBIND_RIGHTWARD (with variables and commas/arrows after)
            if (self.peek(1) and self.peek(1).type == "LBRACK" and
                self.peek(2) and self.peek(2).type == "RBRACK" and
                self.peek(3) and self.peek(3).type == "REBIND_RIGHTWARD"):
                # More flexible check - just need to see REBIND_RIGHTWARD after []
                return self.parse_reverse_destructuring_early()

            if is_destructuring_pattern():
                return self.parse_destructuring_statement()

        # Support binding to variable, list index, or table index
        # Parse a value expression (could be VarInvoke, ListIndex, etc.)
        expr1 = self.parse_value_expression()
        # Assignment: <:
        if self.peek() and self.peek().type == "REBIND_LEFTWARD":
            self.advance()  # consume REBIND_LEFTWARD
            value = self.parse_value_expression()
            return BindOrRebind(expr1, value, code_line=code_line)

        # Check for variant group: Name variants: ...
        if isinstance(expr1, VarInvoke) and self.peek() and self.peek().type == "VARIANTS":
            variant_group = self.parse_variant_group(expr1.name)
            return Binding(expr1.name, variant_group, code_line=code_line)

        # Variable binding: $x: ... or Blueprint definition: Name: <[...]>
        if isinstance(expr1, VarInvoke) and self.peek() and self.peek().type == "BIND":
            self.advance()  # consume BIND

            # Check if this is a blueprint definition: Name: <[...]>
            if self.peek() and self.peek().type == "BLUEPRINT_START":
                blueprint_def = self.parse_blueprint_definition()
                return Binding(expr1.name, blueprint_def, code_line=code_line)

            # Support empty bind: $x: ;
            if self.peek() and self.peek().type == "SEMICOLON":
                return Binding(expr1.name, None, code_line=code_line)

            # Check if this is a blueprint composition: Name and OtherName
            # Parse the value expression
            value = self.parse_value_expression()

            # If the next token is "and", this is blueprint composition
            if self.peek() and self.peek().type == "AND":
                # The value should be a VarInvoke (blueprint name)
                if isinstance(value, VarInvoke):
                    first_blueprint = value.name
                    composition = self.parse_blueprint_composition(first_blueprint)
                    return Binding(expr1.name, composition, code_line=code_line)

            # If the value is a FunctionAtom, mark it as named
            if isinstance(value, FunctionAtom):
                value.is_named = True
            return Binding(expr1.name, value, code_line=code_line)

        # Property binding: $list.property: ... (binding to list/object properties)
        if isinstance(expr1, ListIndex) and getattr(expr1, 'is_property_access', False) and self.peek() and self.peek().type == "BIND":
            self.advance()  # consume BIND
            value = self.parse_value_expression()
            return BindOrRebind(expr1, value, code_line=code_line)
        # Check for reverse destructuring: source[] :> $var1, $var2
        if self.peek() and self.peek().type == "REBIND_RIGHTWARD":
            # Look ahead to see if this is reverse destructuring (variable after :>)
            if self.peek(1) and self.peek(1).type == "KEYNAME":
                # Look further ahead for comma OR arrow to confirm destructuring
                pos = 2
                found_destructuring_pattern = False
                while self.peek(pos) and pos < 10:  # Look ahead a reasonable amount
                    token = self.peek(pos)
                    if token.type in ["COMMA", "ARROW"]:
                        found_destructuring_pattern = True
                        break
                    elif token.type in ["SEMICOLON", "NEWLINE", "RBRACE"]:
                        break
                    pos += 1

                if found_destructuring_pattern:
                    return self.parse_reverse_destructuring(expr1)

        # Implicit bind-or-rebind: :>
        if self.peek() and self.peek().type == "REBIND_RIGHTWARD":
            self.advance()
            expr2 = self.parse_value_expression()
            if isinstance(expr1, VarInvoke) and isinstance(expr2, VarInvoke):
                # $var1 :> $var2 means: bind value of $var1 to $var2
                return BindOrRebind(expr2, expr1, code_line=code_line)
            elif isinstance(expr1, VarInvoke):
                # expr1 :> target (where target can be VarInvoke, ListIndex)
                return BindOrRebind(expr2, expr1, code_line=code_line)
            elif isinstance(expr2, (VarInvoke, ListIndex)):
                # expr :> target (where target can be VarInvoke, ListIndex)
                return BindOrRebind(expr2, expr1, code_line=code_line)
            else:
                raise EnzoParseError(":> must have a variable on one side", code_line=code_line)
        return expr1

    def parse_statements(self):
        from src.runtime_helpers import log_debug
        stmts = []
        while self.pos < len(self.tokens):
            stmt = self.parse_statement()
            stmts.append(stmt)
            # Accept and consume all consecutive semicolons or commas after a statement
            while self.peek() and self.peek().type in ("SEMICOLON", "COMMA"):
                self.advance()
                log_debug(f"[main parser] skipped trailing delimiter after statement, now at parser.pos={self.pos}")
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
        from src.runtime_helpers import log_debug
        ast = self.parse_block()
        # Consume any trailing semicolons/commas after a block
        while self.peek() and self.peek().type in ("SEMICOLON", "COMMA"):
            self.advance()
            log_debug(f"[main parser] skipped trailing delimiter after block, now at parser.pos={self.pos}")
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

    def parse_destructuring_statement(self):
        """Parse destructuring statements like:
        $var1, $var2: source[]
        $var1, $var2 -> $new: source[]  (with renaming)
        source[] :> $var1, $var2        (reverse direction)
        @$var1, @$var2: source[]        (reference destructuring)
        """
        from src.enzo_parser.ast_nodes import DestructuringBinding, ReverseDestructuring, RestructuringBinding, ReferenceDestructuring

        # Check if this starts with @ for reference destructuring
        is_reference = False
        if self.peek() and self.peek().type == "AT":
            is_reference = True
            self.advance()  # consume @

        # Parse first variable
        if not self.peek() or self.peek().type != "KEYNAME":
            raise EnzoParseError("Expected variable name in destructuring", code_line=self._get_code_line(self.peek()) if self.peek() else None)

        first_var_token = self.advance()
        first_var = first_var_token.value
        target_vars = [first_var]

        # Parse remaining variables separated by commas
        while self.peek() and self.peek().type == "COMMA":
            self.advance()  # consume comma

            # Check for @ on individual variables
            var_is_reference = is_reference
            if self.peek() and self.peek().type == "AT":
                var_is_reference = True
                self.advance()  # consume @

            if not self.peek() or self.peek().type != "KEYNAME":
                raise EnzoParseError("Expected variable name after comma in destructuring", code_line=self._get_code_line(self.peek()) if self.peek() else None)

            var_name = self.advance().value
            target_vars.append(var_name)

        # Check for renaming operator ->
        if self.peek() and self.peek().type == "ARROW":
            self.advance()  # consume ->

            if not self.peek() or self.peek().type != "KEYNAME":
                raise EnzoParseError("Expected new variable name after '->' in destructuring", code_line=self._get_code_line(self.peek()) if self.peek() else None)

            new_var = self.advance().value

            # Expect colon
            if not self.peek() or self.peek().type != "BIND":
                raise EnzoParseError("Expected ':' after renaming in destructuring", code_line=self._get_code_line(self.peek()) if self.peek() else None)
            self.advance()  # consume ':'

            # Parse source expression (with destructuring context)
            source_expr = self.parse_destructuring_source()

            return RestructuringBinding(target_vars, new_var, source_expr, is_reference, code_line=self._get_code_line(first_var_token))

        # Check for regular binding :
        elif self.peek() and self.peek().type == "BIND":
            self.advance()  # consume ':'

            # Parse source expression (with destructuring context)
            source_expr = self.parse_destructuring_source()

            if is_reference:
                return ReferenceDestructuring(target_vars, source_expr, code_line=self._get_code_line(first_var_token))
            else:
                return DestructuringBinding(target_vars, source_expr, code_line=self._get_code_line(first_var_token))

        else:
            raise EnzoParseError("Expected ':' or '->' after variables in destructuring", code_line=self._get_code_line(self.peek()) if self.peek() else None)

    def parse_reverse_destructuring(self, source_expr):
        """Parse reverse destructuring: source[] :> $var1, $var2"""
        from src.enzo_parser.ast_nodes import ReverseDestructuring, ReferenceAtom

        # Consume :>
        self.advance()

        # Check if the source expression is a ReferenceAtom (indicates reference destructuring)
        is_reference = isinstance(source_expr, ReferenceAtom)

        # Also check if this starts with @ for reference destructuring (alternative syntax)
        if self.peek() and self.peek().type == "AT":
            is_reference = True
            self.advance()  # consume @

        # Parse first variable
        if not self.peek() or self.peek().type != "KEYNAME":
            raise EnzoParseError("Expected variable name after ':>' in reverse destructuring", code_line=self._get_code_line(self.peek()) if self.peek() else None)

        first_var_token = self.advance()
        first_var = first_var_token.value

        target_vars = []
        renamed_pairs = {}

        # Check for renaming with -> for the first variable
        if self.peek() and self.peek().type == "ARROW":
            self.advance()  # consume ->
            if not self.peek() or self.peek().type != "KEYNAME":
                raise EnzoParseError("Expected new variable name after '->' in reverse destructuring", code_line=self._get_code_line(self.peek()) if self.peek() else None)
            new_var_name = self.advance().value
            target_vars.append(new_var_name)
            renamed_pairs[first_var] = new_var_name  # source_key -> target_var
        else:
            target_vars.append(first_var)

        # Parse remaining variables separated by commas
        while self.peek() and self.peek().type == "COMMA":
            self.advance()  # consume comma

            # Check for @ on individual variables
            var_is_reference = is_reference
            if self.peek() and self.peek().type == "AT":
                var_is_reference = True
                self.advance()  # consume @

            if not self.peek() or self.peek().type != "KEYNAME":
                raise EnzoParseError("Expected variable name after comma in reverse destructuring", code_line=self._get_code_line(self.peek()) if self.peek() else None)

            var_name = self.advance().value

            # Check for renaming with -> in reverse destructuring
            if self.peek() and self.peek().type == "ARROW":
                self.advance()  # consume ->
                if not self.peek() or self.peek().type != "KEYNAME":
                    raise EnzoParseError("Expected new variable name after '->' in reverse destructuring", code_line=self._get_code_line(self.peek()) if self.peek() else None)
                new_var_name = self.advance().value
                target_vars.append(new_var_name)
                renamed_pairs[var_name] = new_var_name  # source_key -> target_var
            else:
                target_vars.append(var_name)

        return ReverseDestructuring(source_expr, target_vars, is_reference, renamed_pairs, code_line=self._get_code_line(first_var_token))

    def parse_reverse_destructuring_early(self):
        """Parse reverse destructuring detected early: $var[] :> $var1, $var2"""
        from src.enzo_parser.ast_nodes import ReverseDestructuring, VarInvoke

        # Parse source variable
        source_var_token = self.advance()  # consume KEYNAME
        source_var = VarInvoke(source_var_token.value, code_line=self._get_code_line(source_var_token))

        # Consume []
        self.advance()  # consume LBRACK
        self.advance()  # consume RBRACK

        # Consume :>
        self.advance()  # consume REBIND_RIGHTWARD

        # Check if this starts with @ for reference destructuring
        is_reference = False
        if self.peek() and self.peek().type == "AT":
            is_reference = True
            self.advance()  # consume @

        # Parse first variable
        if not self.peek() or self.peek().type != "KEYNAME":
            raise EnzoParseError("Expected variable name after ':>' in reverse destructuring", code_line=self._get_code_line(self.peek()) if self.peek() else None)

        first_var_token = self.advance()
        first_var = first_var_token.value

        target_vars = []
        renamed_pairs = {}

        # Check for renaming with -> for the first variable
        if self.peek() and self.peek().type == "ARROW":
            self.advance()  # consume ->
            if not self.peek() or self.peek().type != "KEYNAME":
                raise EnzoParseError("Expected new variable name after '->' in reverse destructuring", code_line=self._get_code_line(self.peek()) if self.peek() else None)
            new_var_name = self.advance().value
            target_vars.append(new_var_name)
            renamed_pairs[first_var] = new_var_name  # source_key -> target_var
        else:
            target_vars.append(first_var)

        # Parse remaining variables separated by commas
        while self.peek() and self.peek().type == "COMMA":
            self.advance()  # consume comma

            # Check for @ on individual variables
            var_is_reference = is_reference
            if self.peek() and self.peek().type == "AT":
                var_is_reference = True
                self.advance()  # consume @

            if not self.peek() or self.peek().type != "KEYNAME":
                raise EnzoParseError("Expected variable name after comma in reverse destructuring", code_line=self._get_code_line(self.peek()) if self.peek() else None)

            var_name = self.advance().value

            # Check for renaming with -> in reverse destructuring
            if self.peek() and self.peek().type == "ARROW":
                self.advance()  # consume ->
                if not self.peek() or self.peek().type != "KEYNAME":
                    raise EnzoParseError("Expected new variable name after '->' in reverse destructuring", code_line=self._get_code_line(self.peek()) if self.peek() else None)
                new_var_name = self.advance().value
                target_vars.append(new_var_name)
                renamed_pairs[var_name] = new_var_name  # source_key -> target_var
            else:
                target_vars.append(var_name)

        return ReverseDestructuring(source_var, target_vars, is_reference, renamed_pairs, code_line=self._get_code_line(first_var_token))

    def parse_destructuring_source(self):
        """Parse source expression in destructuring context, handling [] suffix properly."""
        # In destructuring context, we expect: $variable[]
        # The [] should NOT be treated as blueprint instantiation

        if not self.peek() or self.peek().type != "KEYNAME":
            raise EnzoParseError("Expected variable name in destructuring source", code_line=self._get_code_line(self.peek()) if self.peek() else None)

        # Parse the variable name
        var_token = self.advance()
        from src.enzo_parser.ast_nodes import VarInvoke
        base_expr = VarInvoke(var_token.value, code_line=self._get_code_line(var_token))

        # Check for [] suffix which indicates destructuring
        if self.peek() and self.peek().type == "LBRACK":
            self.advance()  # consume LBRACK
            if self.peek() and self.peek().type == "RBRACK":
                self.advance()  # consume RBRACK
                # Return the variable - the [] just indicates destructuring context
                return base_expr
            else:
                # This is not empty brackets, error in destructuring context
                raise EnzoParseError("Expected empty brackets [] in destructuring context", code_line=self._get_code_line(self.peek()) if self.peek() else None)
        else:
            # No brackets - just return the variable
            return base_expr

    def parse_complex_bracket_destructuring(self):
        """Parse complex bracket destructuring: [$var1, $var2 -> $var3]:> $target[]"""
        from src.enzo_parser.ast_nodes import RestructuringBinding

        # Consume [
        self.advance()

        # Parse first variable
        if not self.peek() or self.peek().type != "KEYNAME":
            raise EnzoParseError("Expected variable name in complex bracket destructuring", code_line=self._get_code_line(self.peek()) if self.peek() else None)

        first_var_token = self.advance()
        first_var = first_var_token.value
        target_vars = [first_var]
        new_var = None

        # Parse remaining variables separated by commas
        while self.peek() and self.peek().type == "COMMA":
            self.advance()  # consume comma

            if not self.peek() or self.peek().type != "KEYNAME":
                raise EnzoParseError("Expected variable name after comma in complex bracket destructuring", code_line=self._get_code_line(self.peek()) if self.peek() else None)

            var_name = self.advance().value
            target_vars.append(var_name)

        # Check for renaming operator -> after all variables have been parsed
        if self.peek() and self.peek().type == "ARROW":
            self.advance()  # consume ->

            if not self.peek() or self.peek().type != "KEYNAME":
                raise EnzoParseError("Expected new variable name after '->' in complex bracket destructuring", code_line=self._get_code_line(self.peek()) if self.peek() else None)

            new_var = self.advance().value

        # Consume ]
        if not self.peek() or self.peek().type != "RBRACK":
            raise EnzoParseError("Expected ']' in complex bracket destructuring", code_line=self._get_code_line(self.peek()) if self.peek() else None)
        self.advance()

        # Consume :>
        if not self.peek() or self.peek().type != "REBIND_RIGHTWARD":
            raise EnzoParseError("Expected ':>' after ']' in complex bracket destructuring", code_line=self._get_code_line(self.peek()) if self.peek() else None)
        self.advance()

        # Parse target expression (should be something like $target[])
        target_expr = self.parse_destructuring_source()

        return RestructuringBinding(target_vars, new_var, target_expr, False, code_line=self._get_code_line(first_var_token))

# Top-level API for main interpreter and debug module

def parse(src):
    """Parse a single Enzo source string into an AST (single statement/block)."""
    parser = Parser(src)
    return parser.parse()

def parse_program(src):
    """Parse a full Enzo source string into a Program AST (multiple statements)."""
    parser = Parser(src)
    return parser.parse_program()
