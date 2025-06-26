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
    debug=True
)


class AST(Transformer):
    def param_binding(self, items):
        # Always: [PARAM, NAME, expr], may get as tokens or tree, so just always pick last two.
        # items[0] == PARAM (Token or str), items[1] == NAME (Token), items[2] == expr
        name_tok = items[1]
        expr = items[2]
        return ("param", name_tok.value, expr)

    # ── Top‐level “start” folds into a block of statements ───────────────
    def start(self, v):
        # v is a list of AST nodes for each semicolon‐terminated stmt.
        # Instead of returning only the last one, we return ("block", [stmt1, stmt2, …]).
        v = [x for x in v if not isinstance(x, Token)]
        return ("block", v)

    def stmt(self, v):
        # Only allow top-level atoms as statements, plus assignments/rebinds
        node = v[0]
        # Disallow 'return' at top level!
        if isinstance(node, tuple):
            tag = node[0]
            if tag == "return":
                raise SyntaxError("return(...) is only allowed inside block expressions, not at the top level.")
            if tag in ("bind", "rebind", "bind_empty", "number_atom", "text_atom", "list", "table", "block_expr", "expr"):
                return node
            # If we ever see ("expr", ...) at top-level, only allow if it's an atom inside
            if tag == "expr":
                inner = node[1]
                if isinstance(inner, tuple) and inner[0] in ("number_atom", "text_atom", "list", "table", "block_expr"):
                    return node
        # If we get here, this was an illegal top-level non-atom expr
        raise SyntaxError("Only atoms (number atom, text atom, list, table, function/block) are allowed as top-level statements. Wrap expressions in parens.")

    # ── literals ─────────────────────────────────────────────────────────
    def number_atom(self, tok):
        # tok[0] is a string like '42' or '-3'
        return ("number_atom", int(tok[0]))

    def text_atom(self, tok):
        # tok[0] looks like '"hello"', so strip the outer quotes
        return ("text_atom", tok[0][1:-1])

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
    # table_item: NAME ":" expr
    #   key_tok.value is something like "$foo"
    def table_item(self, v):
        key_tok, val_node = v
        # Keep leading "$" on the property name
        return (key_tok.value, val_node)

    def table(self, pairs):
        # pairs will be [] for {}, or [table_item_list] for { ... }
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

    def function_item(self, items):
        # Flatten nested items (needed for some edge-cases in param/return)
        if isinstance(items, list) and len(items) == 1:
            return items[0]
        return items

    def function_body(self, items):
        # Remove tokens, flatten nested lists, filter only AST nodes
        flat = []
        for x in items:
            if x is None:
                continue
            if isinstance(x, Token):
                continue
            if isinstance(x, list):
                for y in x:
                    if y is None or isinstance(y, Token):
                        continue
                    flat.append(y)
            else:
                flat.append(x)
        return flat

    def function_local_var(self, items):
        name_tok, expr = items
        return ("function_local_var", name_tok.value, expr)

    def block_sep(self, items):
        # Ignore block separators in block_body
        return None


    def block_expr(self, items):
        # Flatten block items into params, bindings, stmts (ignore any Tokens or nested lists)
        params = []
        bindings = []
        stmts = []

        def extract_block_parts(block):
            if not isinstance(block, tuple):
                return
            if block[0] == "block_expr":
                stmts.append(block)
            elif block[0] == "param":
                params.append((block[1], block[2]))
            elif block[0] == "function_local_var":
                bindings.append((block[1], block[2]))
            elif block[0] == "bind_empty":
                bindings.append((block[1], None))
            else:
                stmts.append(block)

        for it in items:
            # Filter out tokens/lists here too
            if it is None or isinstance(it, Token):
                continue
            if isinstance(it, list):
                for sub in it:
                    extract_block_parts(sub)
            else:
                extract_block_parts(it)

        is_multiline = False  # (can be updated if you want later)
        return ("block_expr", params, bindings, stmts, is_multiline)



    def call(self, v):
        name_tok = v[0]
        args = v[1] if len(v) > 1 else []
        # Support NAME (Token), FUNCNAME (Token), or ("var", "$foo")
        if hasattr(name_tok, 'value'):
            name = name_tok.value
        elif isinstance(name_tok, str):
            name = name_tok
        elif isinstance(name_tok, tuple):
            # If it's ("var", "$foo")
            if len(name_tok) >= 2:
                name = name_tok[1]
            else:
                raise Exception(f"Unexpected call node form: {name_tok!r}")
        else:
            raise Exception(f"Unknown call target: {name_tok!r}")
        return ("call", name, args)

    def function_arg_list(self, v):
        return v

    def return_stmt(self, v):
        # Just grab the second item, which is the expr
        return ("return", v[-1])

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
                # e.g. ".3" → literal integer 3 (as plain int, not number_atom)
                idx_node = int(t[1:])
                node = ("index", node, idx_node)

            elif isinstance(t, Token) and t.type == "DOTVAR":
                # e.g. ".$foo" → lookup variable $foo
                var_name = t[1:]
                node = ("index", node, ("var", var_name))

            elif isinstance(t, Token) and t.type == "DOTPROP":
                # e.g. ".foo" → property access
                prop_name = t[1:]
                node = ("attr", node, prop_name)

            else:
                raise Exception(f"Unknown index_chain token: {t!r}")
        return node

    # ── statements / assignments ─────────────────────────────────────────────────
    def bind(self, v):
        name_tok, expr_node = v
        return ("bind", name_tok.value, expr_node)

    def bind_func(self, v):
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

    def table_item_list(self, items):
        # print("TABLE DEBUG: kvlist =", kvlist)
        # Remove Nones and Trees for kvpair_sep and any other non-tuple junk
        return [x for x in items if isinstance(x, tuple) and len(x) == 2]


def parse(src: str):
    return AST().transform(_parser.parse(src))
