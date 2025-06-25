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
    def function_param(self, items):
        # Always: [PARAM, NAME, expr], may get as tokens or tree, so just always pick last two.
        # items[0] == PARAM (Token or str), items[1] == NAME (Token), items[2] == expr
        name_tok = items[1]
        expr = items[2]
        return ("function_param", name_tok.value, expr)

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
                raise SyntaxError("return(...) is only allowed inside function atoms, not at the top level.")
            if tag in ("bind", "rebind", "bind_empty", "number", "text", "list", "table", "function_atom", "expr"):
                return node
            # If we ever see ("expr", ...) at top-level, only allow if it's an atom inside
            if tag == "expr":
                inner = node[1]
                if isinstance(inner, tuple) and inner[0] in ("number", "text", "list", "table", "function_atom"):
                    return node
        # If we get here, this was an illegal top-level non-atom expr
        raise SyntaxError("Only atoms (number, string, list, table, function/block) are allowed as top-level statements. Wrap expressions in parens.")

    # ── literals ─────────────────────────────────────────────────────────
    def number(self, tok):
        return ("number", int(tok[0]))

    def string(self, tok):
        # tok[0] looks like "\"hello\"", so strip the outer quotes
        return ("text", tok[0][1:-1])

    def list(self, vals):
        # Lark gives: vals == [] for [], or [atom_list] for [a, ...]
        # atom_list is [] for [ ], or [item, ...] for [a, ...]
        if not vals or vals == [None]:
            return ("list", [])
        # Accept both [atom_list] and atom_list directly
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

    def block_body(self, items):
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

    def function_item(self, items):
        # Flatten nested items (needed for some edge-cases in param/return)
        if isinstance(items, list) and len(items) == 1:
            return items[0]
        return items

    def function_local_binding(self, items):
        name_tok, expr = items
        return ("bind", name_tok.value, expr)

    def function_separator(self, items):
        # Ignore block separators in block_body
        return None


    def function_atom_single(self, items):
        # items is a Tree or list, possibly deeply nested.
        # Always unwrap to tuple here!
        if isinstance(items, list) and len(items) == 1 and isinstance(items[0], tuple) and items[0][0] == "function_atom":
            return items[0]  # Already transformed!
        params, bindings, stmts = self._block_parts(items)
        return ("function_atom", params, bindings, stmts, False)

    def function_atom_multi(self, items):
        # Always unwrap to tuple here!
        if isinstance(items, list) and len(items) == 1 and isinstance(items[0], tuple) and items[0][0] == "function_atom":
            return items[0]  # Already transformed!
        params, bindings, stmts = self._block_parts(items)
        return ("function_atom", params, bindings, stmts, True)

    def _block_parts(self, items):
        # Flatten function items into params, bindings, stmts
        params, bindings, stmts = [], [], []
        def extract_block_parts(block):
            if not isinstance(block, tuple):
                return [], [], [block]
            if block[0] == "function_atom":
                inner_params, inner_bindings, inner_stmts, _ = block[1:]
                return inner_params, inner_bindings, inner_stmts
            elif block[0] == "function_param":
                return [ (block[1], block[2]) ], [], []
            elif block[0] == "bind":
                return [], [ (block[1], block[2]) ], []
            elif block[0] == "bind_empty":
                return [], [ (block[1], None) ], []
            else:
                return [], [], [block]
        for it in items:
            if it is None or isinstance(it, Token):
                continue
            if isinstance(it, list):
                for sub in it:
                    if sub is None or isinstance(sub, Token):
                        continue
                    p, b, s = extract_block_parts(sub)
                    params += p
                    bindings += b
                    stmts += s
            else:
                p, b, s = extract_block_parts(it)
                params += p
                bindings += b
                stmts += s
        return params, bindings, stmts



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

    def return_statement(self, v):
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
                # e.g. ".3" → literal integer 3
                idx_node = ("number", int(t[1:]))
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

    def bind_function(self, v):
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

    def atom_statement(self, v):
        # wrap a bare expression into (“expr”, AST)
        return ("expr", v[0])

    def atom_list(self, items):
        # Only keep actual expr nodes (usually tuples, ints, or str)
        return [x for x in items if isinstance(x, (tuple, int, str))]

    def table_item_list(self, items):
        # print("TABLE DEBUG: kvlist =", kvlist)
        # Remove Nones and Trees for table_separator and any other non-tuple junk
        return [x for x in items if isinstance(x, tuple) and len(x) == 2]


def ast_sanitize(node):
    from lark import Tree, Token
    if isinstance(node, Tree):
        # Recursively convert Lark Tree to tuple of its sanitized children
        return tuple(ast_sanitize(c) for c in node.children)
    elif isinstance(node, Token):
        # Always extract .value from Tokens
        return node.value
    elif isinstance(node, list):
        return [ast_sanitize(x) for x in node]
    elif isinstance(node, tuple):
        return tuple(ast_sanitize(x) for x in node)
    elif isinstance(node, dict):
        return {k: ast_sanitize(v) for k, v in node.items()}
    else:
        return node

def parse(src: str):
    tree = _parser.parse(src)
    ast = AST().transform(tree)
    return ast_sanitize(ast)
