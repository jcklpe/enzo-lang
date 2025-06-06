from pathlib import Path
from lark import Tree, Lark, Transformer, Token

# ───────────────────────────
# Load the grammar (grammar.lark must already be in place)
# ───────────────────────────
_parser = Lark(
    Path(__file__).with_name("grammar.lark").read_text(),
    parser="lalr",
    start="start",
)


class AST(Transformer):
    # ── Top‐level “start” folds into a block of statements ───────────────
    def start(self, v):
        # v is a list of AST nodes for each semicolon‐terminated stmt.
        # Instead of returning only the last one, we return ("block", [stmt1, stmt2, …]).
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
        # Lark: vals is [] for [], or [expr_list] for [a, b, ...]
        # expr_list is [] for [ ], [item, ...] for [a, ...], [None] for [ , ]
        if not vals or vals == [None]:
            return ("list", [])
        # If we get a [None], treat it as empty list
        items = vals[0] if isinstance(vals[0], list) else vals
        if items == [None]:
            items = []
        return ("list", items)

    # ── table literal ───────────────────────────────────────────────────
    # kvpair: KEY ":" expr
    #   key_tok.value is something like "$foo"
    def kvpair(self, v):
        key_tok, val_node = v
        # Keep leading "$" on the property name
        return (key_tok.value, val_node)

    def table(self, pairs):
        # Lark: pairs is [] for {}, or [kvpair_list] for {...}
        # kvpair_list is [] for { }, [item, ...] for {a: b, ...}, [None] for { , }
        if not pairs or pairs == [None]:
            return ("table", {})
        kvlist = pairs[0] if isinstance(pairs[0], list) else pairs
        if kvlist == [None]:
            kvlist = []
        d = {}
        for item in kvlist:
            if not isinstance(item, tuple) or len(item) != 2:
                raise ValueError(f"Invalid kvpair in table: {item!r}")
            key, val_node = item
            d[key] = val_node
        return ("table", d)

    def var(self, tok):
        # tok[0].value is something like "$foo"
        return ("var", tok[0].value)

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
        # v is a single‐element list: [Token(NAME)]
        name_tok = v[0]
        return ("bind_empty", name_tok.value)

    def rebind(self, v):
        name_tok, expr_node = v
        return ("rebind", name_tok.value, expr_node)

    def prop_rebind(self, v):
        # v = [ baseAST(for something like $tbl.name), newExprAST ]
        base_node, new_expr = v
        return ("prop_rebind", base_node, new_expr)

    def rebind_lr(self, v):
        expr_node, name_tok = v
        return ("rebind", name_tok.value, expr_node)

    def expr_stmt(self, v):
        # wrap a bare expression into (“expr”, AST)
        return ("expr", v[0])

    def expr_list(self, items):
        # Remove stray Nones (from trailing commas)
        return [x for x in items if x is not None]

    def kvpair_list(self, items):
        # Remove stray Nones (from trailing commas)
        return [x for x in items if x is not None]


def parse(src: str):
    return AST().transform(_parser.parse(src))
