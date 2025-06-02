from pathlib import Path
from lark import Lark, Transformer, Token

_parser = Lark(
    Path(__file__).with_name("grammar.lark").read_text(),
    parser="lalr",
    start="start",
)

class AST(Transformer):
    # ── literals ────────────────────────────────────
    def number(self, tok):
        return ("num", int(tok[0]))

    def string(self, tok):
        # tok[0] is the raw Lark string literal, e.g. "\"hello\""
        return ("str", tok[0][1:-1])  # strip surrounding quotes

    def list(self, vals):
        return ("list", vals)

    # ── table literal ──────────────────────────────
    # kvpair: KEY ":" expr
    #   key_tok.value is something like "$foo"
    def kvpair(self, v):
        key_tok, val_node = v
        # Keep the leading "$" on the property name:
        return (key_tok.value, val_node)

    def table(self, pairs):
        # pairs is a list of (key_stringWithDollar, exprNode)
        return ("table", dict(pairs))

    def var(self, tok):
        # tok[0].value is something like "$foo"
        return ("var", tok[0].value)

    # ── arithmetic ─────────────────────────────────
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

    # ── selector chain: handles .INT, .VAR, .PROP ──
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
                # Keep the leading "$" on the var‐name:
                idx_node = ("var", t.value[1:])   # t.value is ".$foo", so [1:] == "$foo"
                node = ("index", node, idx_node)

            elif isinstance(t, Token) and t.type == "DOTPROP":
                # e.g. ".foo" → attribute access of key "$foo"
                prop_name = "$" + t.value[1:]    # t.value is ".foo", so t.value[1:] == "foo"
                node = ("attr", node, prop_name)

            else:
                # Should never happen, but just in case:
                raise ValueError(f"Unexpected token in index_chain: {t!r}")

        return node

    # ── statements / assignments ───────────────────────────
    def bind(self, v):
        name_tok, expr_node = v
        return ("bind", name_tok.value, expr_node)

    def rebind(self, v):
        name_tok, expr_node = v
        return ("rebind", name_tok.value, expr_node)

    def prop_rebind(self, v):
        # v = [ baseAST(for $tbl.name), newExprAST ]
        base_node, new_expr = v
        return ("prop_rebind", base_node, new_expr)

    def rebind_lr(self, v):
        expr_node, name_tok = v
        return ("rebind", name_tok.value, expr_node)

    def expr_stmt(self, v):
        return ("expr", v[0])


def parse(src: str):
    return AST().transform(_parser.parse(src))
