# AST node definitions for Enzo custom parser

class ASTNode:
    def __init__(self, code_line=None):
        self.code_line = code_line

class Program(ASTNode):
    def __init__(self, statements, code_line=None):
        super().__init__(code_line)
        self.statements = statements
    def __repr__(self):
        return f"Program(statements={self.statements!r})"

class FunctionAtom(ASTNode):
    def __init__(self, params, local_vars, body, context=None, code_line=None, is_multiline=False):
        super().__init__(code_line)
        self.params = params
        self.local_vars = local_vars
        self.body = body
        self.context = context  # e.g., 'statement', 'binding', 'expression'
        self.is_multiline = is_multiline  # True if function atom spans multiple lines
    def __repr__(self):
        return f"FunctionAtom(params={self.params!r}, local_vars={self.local_vars!r}, body={self.body!r}, context={self.context!r}, is_multiline={self.is_multiline!r})"

class Binding(ASTNode):
    def __init__(self, name, value, code_line=None):
        super().__init__(code_line)
        self.name = name
        self.value = value
    def __repr__(self):
        return f"Binding(name={self.name!r}, value={self.value!r})"

class Invoke(ASTNode):
    def __init__(self, func, args, code_line=None):
        super().__init__(code_line)
        self.func = func
        self.args = args
    def __repr__(self):
        return f"Invoke(func={self.func!r}, args={self.args!r})"

class TableAtom(ASTNode):
    def __init__(self, items, code_line=None):
        super().__init__(code_line)
        self.items = items
    def __repr__(self):
        # Warn if this is ever printed directly
        return f"<TableAtom(items={self.items!r})>"

class NumberAtom(ASTNode):
    def __init__(self, value, code_line=None):
        super().__init__(code_line)
        self.value = value
    def __repr__(self):
        return f"NumberAtom(value={self.value!r})"

class TextAtom(ASTNode):
    def __init__(self, value, code_line=None):
        super().__init__(code_line)
        self.value = value
    def __repr__(self):
        return f"TextAtom(value={self.value!r})"

class ListAtom(ASTNode):
    def __init__(self, elements, code_line=None):
        super().__init__(code_line)
        self.elements = elements
    def __repr__(self):
        return f"ListAtom(elements={self.elements!r})"

class ListKeyValue(ASTNode):
    def __init__(self, keyname, value, code_line=None):
        super().__init__(code_line)
        self.keyname = keyname
        self.value = value
    def __repr__(self):
        return f"ListKeyValue(keyname={self.keyname!r}, value={self.value!r})"

class VarInvoke(ASTNode):
    def __init__(self, name, code_line=None):
        super().__init__(code_line)
        self.name = name
    def __repr__(self):
        return f"VarInvoke(name={self.name!r})"

class AddNode(ASTNode):
    def __init__(self, left, right, code_line=None):
        super().__init__(code_line)
        self.left = left
        self.right = right
    def __repr__(self):
        return f"AddNode(left={self.left!r}, right={self.right!r})"

class SubNode(ASTNode):
    def __init__(self, left, right, code_line=None):
        super().__init__(code_line)
        self.left = left
        self.right = right
    def __repr__(self):
        return f"SubNode(left={self.left!r}, right={self.right!r})"

class MulNode(ASTNode):
    def __init__(self, left, right, code_line=None):
        super().__init__(code_line)
        self.left = left
        self.right = right
    def __repr__(self):
        return f"MulNode(left={self.left!r}, right={self.right!r})"

class DivNode(ASTNode):
    def __init__(self, left, right, code_line=None):
        super().__init__(code_line)
        self.left = left
        self.right = right
    def __repr__(self):
        return f"DivNode(left={self.left!r}, right={self.right!r})"

class BindOrRebind(ASTNode):
    def __init__(self, target, value, code_line=None):
        super().__init__(code_line)
        self.target = target  # variable name (string)
        self.value = value    # value expression
    def __repr__(self):
        return f"BindOrRebind(target={self.target!r}, value={self.value!r})"

class FunctionRef(ASTNode):
    def __init__(self, expr, code_line=None):
        super().__init__(code_line)
        self.expr = expr  # Can be a VarInvoke, TableIndex, or other expression
    def __repr__(self):
        return f"FunctionRef(expr={self.expr!r})"

class ListIndex(ASTNode):
    def __init__(self, base, index, code_line=None):
        super().__init__(code_line)
        self.base = base  # The list expression
        self.index = index  # The index expression (should be NumberAtom or VarInvoke)
    def __repr__(self):
        return f"ListIndex(base={self.base!r}, index={self.index!r})"

class TableIndex(ASTNode):
    def __init__(self, base, key, code_line=None):
        super().__init__(code_line)
        self.base = base  # The table expression
        self.key = key    # The key (should be a string or VarInvoke)
    def __repr__(self):
        return f"TableIndex(base={self.base!r}, key={self.key!r})"

class ReturnNode(ASTNode):
    def __init__(self, value, code_line=None):
        super().__init__(code_line)
        self.value = value
    def __repr__(self):
        return f"ReturnNode(value={self.value!r})"

class PipelineNode(ASTNode):
    def __init__(self, left, right, code_line=None):
        super().__init__(code_line)
        self.left = left   # The expression to pipe
        self.right = right # The function atom to receive the value
    def __repr__(self):
        return f"PipelineNode(left={self.left!r}, right={self.right!r})"

class ParameterDeclaration(ASTNode):
    def __init__(self, name, default_value, code_line=None):
        super().__init__(code_line)
        self.name = name
        self.default_value = default_value
    def __repr__(self):
        return f"ParameterDeclaration(name={self.name!r}, default_value={self.default_value!r})"
# ...add more as needed
