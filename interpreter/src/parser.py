from pathlib import Path
from lark import Tree, Lark, Transformer, Token

# ───────────────────────────
# Load the grammar (grammar.lark must already be in place)
# ───────────────────────────
grammar_path = Path(__file__).with_name("grammar.lark")
# print("GRAMMAR PATH:", grammar_path.absolute())
# print("LOADING LARK PARSER in src/parser.py")
_parser = Lark(
    grammar_path.read_text(),
    parser="lalr",
    start="start",
)


class AST(Transformer):
    def param_binding(self, items):
        name_tok, expr = items
        return ("param", name_tok.value, expr)
    # ── Top‐level “start” folds into a block of statements ───────────────
    def start(self, v):
        # v is a list of AST nodes for each semicolon‐terminated stmt.
        # Instead of returning only the last one, we return ("block", [stmt1, stmt2, …]).
        v = [x for x in v if not isinstance(x, Token)]
        return ("block", v)

    def stmt(self, v):
        # unwrap a single statement into its AST (either bind, rebind, expr, etc.)
        return v[0]

    # ── literals ─────────────────────────────────────────────────────────
    def number(self, tok):
        return ("num", int(tok[0]))

    def string(self, tok):
        # tok[0] looks like "\"hello\"", so strip the outer quotes
        return ("str", tok[0][1:-1])

    def list(self, vals):
        # Lark gives: vals == [] for [], or [expr_list] for [a, ...]
        # expr_list is [] for [ ], or [item, ...] for [a, ...]
        if not vals or vals == [None]:
            return ("list", [])
        # Accept both [expr_list] and expr_list directly
        items = vals[0] if isinstance(vals[0], list) else vals
        if items == [None]:
            items = []
        return ("list", items)

    # ── table literal ───────────────────────────────────────────────────
    # kvpair: NAME ":" expr
    #   key_tok.value is something like "$foo"
    def kvpair(self, v):
        key_tok, val_node = v
        # Keep leading "$" on the property name
        return (key_tok.value, val_node)

    def table(self, pairs):
        # pairs will be [] for {}, or [kvpair_list] for { ... }
        if not pairs or pairs == [None]:
            return ("table", {})
        # Sometimes pairs is [[...]], sometimes it's just [...]
        def flatten(l):
            for x in l:
                if isinstance(x, list):
                    yield from flatten(x)
                elif isinstance(x, tuple) and len(x) == 2:
                    yield x
                # else: ignore anything else (like tokens, Nones, etc)
        kvlist = list(flatten(pairs))
        d = {}
        for key, val_node in kvlist:
            d[key] = val_node
        return ("table", d)

    def var(self, tok):
        # tok[0].value is something like "$foo"
        return ("var", tok[0].value)

    def block_body(self, items):
        # filter out separators AND newlines
        return [x for x in items if x is not None and not (isinstance(x, Token) and x.type == "NEWLINE")]

    def block_item(self, items):
        return items[0]

    def block_binding(self, items):
        name_tok, expr = items
        return ("bind", name_tok.value, expr)

    def block_sep(self, items):
        # Ignore block separators in block_body
        return None


    def block_expr(self, items):
        # Always force the body to be a flat list of AST tuples
        lpar_token, rpar_token = None, None
        body = None

        for it in items:
            if isinstance(it, Token) and it.type == "LPAR":
                lpar_token = it
            elif isinstance(it, Token) and it.type == "RPAR":
                rpar_token = it
            elif isinstance(it, Tree) and it.data == "block_body":
                body = [self._transform_child(x) for x in it.children]
            elif isinstance(it, list):
                body = it
            elif isinstance(it, tuple):
                body = [it]

        # Fallback: body is just the items
        if body is None:
            body = []
            for i in items:
                if isinstance(i, (tuple, Tree)):
                    body.append(i)

        # If tokens weren't found, fake them (for grouped exprs, etc.)
        if lpar_token is None:
            lpar_token = Token("LPAR", "(", 0, 0, 0)
        if rpar_token is None:
            rpar_token = Token("RPAR", ")", 0, 0, 0)

        params = []
        bindings = []
        stmts = []
        for part in body:
            if isinstance(part, tuple) and part:
                tag = part[0]
                if tag == "param":
                    params.append((part[1], part[2]))
                elif tag == "bind":
                    bindings.append((part[1], part[2]))
                elif tag == "bind_empty":
                    bindings.append((part[1], None))
                else:
                    stmts.append(part)
            else:
                stmts.append(part)
        is_multiline = lpar_token.line != rpar_token.line
        return ("block_expr", params, bindings, stmts, is_multiline)



    def call(self, v):
        name_tok = v[0]
        args = v[1] if len(v) > 1 else []
        return ("call", name_tok.value, args)

    def call_args(self, v):
        return v

    def return_stmt(self, v):
        return ("return", v[0])

    # ── arithmetic ───────────────────────────────────────────────────────
    def add(self, v):
        return ("add", *v)

    def sub(self, v):
        return ("sub", *v)

    def mul(self, v):
        return ("mul", *v)

    def div(self, v):
        return ("div", *v)

    def paren(self, v):
        return v[0]

    # ── selector chain: (.3, .$foo, .prop) ─────────────────────────────
    def index_chain(self, v):
        base, *toks = v
        node = base
        for t in toks:
            if isinstance(t, Token) and t.type == "DOTINT":
                # e.g. ".3" → literal integer 3
                idx_node = ("num", int(t[1:]))
                node = ("index", node, idx_node)

            elif isinstance(t, Token) and t.type == "DOTVAR":
                # e.g. ".$foo" → lookup variable $foo
                # t.value == ".$foo", so [1:] == "$foo"
                idx_node = ("var", t.value[1:])
                node = ("index", node, idx_node)

            elif isinstance(t, Token) and t.type == "DOTPROP":
                # e.g. ".foo" → attribute access of key "$foo"
                prop_name = "$" + t.value[1:]  # t.value==".foo", so t.value[1:]=="foo"
                node = ("attr", node, prop_name)

            else:
                raise ValueError(f"Unexpected token in index_chain: {t!r}")

        return node

    # ── statements / assignments ─────────────────────────────────────────────────
    def bind(self, v):
        name_tok, expr_node = v
        return ("bind", name_tok.value, expr_node)

    def bind_empty(self, v):
        name_tok = v[0]
        return ("bind_empty", name_tok.value)

    def rebind(self, v):
        name_tok, expr_node = v
        return ("rebind", name_tok.value, expr_node)

    def rebind_lr(self, v):
        expr_node, name_tok = v
        return ("rebind", name_tok.value, expr_node)

    def prop_rebind(self, v):
        # v = [ baseAST(for something like $tbl.name), newExprAST ]
        base_node, new_expr = v
        return ("prop_rebind", base_node, new_expr)

    def expr_stmt(self, v):
        # wrap a bare expression into (“expr”, AST)
        return ("expr", v[0])

    def expr_list(self, items):
        # Only keep actual expr nodes (usually tuples, ints, or str)
        return [x for x in items if isinstance(x, (tuple, int, str))]

    def kvpair_list(self, items):
        # print("TABLE DEBUG: kvlist =", kvlist)
        # Remove Nones and Trees for kvpair_sep and any other non-tuple junk
        return [x for x in items if isinstance(x, tuple) and len(x) == 2]


def parse(src: str):
    return AST().transform(_parser.parse(src))
