# AST node definitions for Enzo custom parser

class ASTNode:
    pass

class Program(ASTNode):
    def __init__(self, statements):
        self.statements = statements
    def __repr__(self):
        return f"Program(statements={self.statements!r})"

class FunctionAtom(ASTNode):
    def __init__(self, params, local_vars, body, context=None):
        self.params = params
        self.local_vars = local_vars
        self.body = body
        self.context = context  # e.g., 'statement', 'binding', 'expression'
    def __repr__(self):
        return f"FunctionAtom(params={self.params!r}, local_vars={self.local_vars!r}, body={self.body!r}, context={self.context!r})"

class Binding(ASTNode):
    def __init__(self, name, value):
        self.name = name
        self.value = value
    def __repr__(self):
        return f"Binding(name={self.name!r}, value={self.value!r})"

class Invoke(ASTNode):
    def __init__(self, func, args):
        self.func = func
        self.args = args
    def __repr__(self):
        return f"Invoke(func={self.func!r}, args={self.args!r})"

class TableAtom(ASTNode):
    def __init__(self, items):
        self.items = items
    def __repr__(self):
        return f"TableAtom(items={self.items!r})"

class NumberAtom(ASTNode):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"NumberAtom(value={self.value!r})"

class TextAtom(ASTNode):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return f"TextAtom(value={self.value!r})"

class ListAtom(ASTNode):
    def __init__(self, elements):
        self.elements = elements
    def __repr__(self):
        return f"ListAtom(elements={self.elements!r})"

class VarInvoke(ASTNode):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f"VarInvoke(name={self.name!r})"

class AddNode(ASTNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return f"AddNode(left={self.left!r}, right={self.right!r})"

class SubNode(ASTNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return f"SubNode(left={self.left!r}, right={self.right!r})"

class MulNode(ASTNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return f"MulNode(left={self.left!r}, right={self.right!r})"

class DivNode(ASTNode):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return f"DivNode(left={self.left!r}, right={self.right!r})"

class BindOrRebind(ASTNode):
    def __init__(self, target, value):
        self.target = target  # variable name (string)
        self.value = value    # value expression
    def __repr__(self):
        return f"BindOrRebind(target={self.target!r}, value={self.value!r})"
# ...add more as needed
