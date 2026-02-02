"""
Pygments lexer for Enzo language syntax highlighting
"""

from pygments.lexer import RegexLexer, bygroups, words, include
from pygments.token import (
    Comment, Keyword, Name, Number, Operator, Punctuation,
    String, Text, Whitespace, Generic
)

class EnzoLexer(RegexLexer):
    """
    Lexer for the Enzo programming language
    """
    name = 'Enzo'
    aliases = ['enzo']
    filenames = ['*.enzo']

    tokens = {
        'root': [
            # Whitespace
            (r'\s+', Whitespace),

            # Block comments /` ... `/
            (r"/'.*?'/", Comment.Multiline),

            # Single line comments
            (r'//=.*?$', Comment.Special),  # Test markers
            (r'//.*?$', Comment.Single),

            # Variable references (@variable) - must come before @ operator
            (r'@[a-zA-Z_\-][a-zA-Z0-9_\-]*', Name.Decorator),

            # Variables ($variable) - must come before other operators
            (r'\$[a-zA-Z_\-0-9][a-zA-Z0-9_\-]*', Name.Variable),

            # Keywords - control flow
            (words((
                'If', 'Else', 'For', 'While', 'end', 'Loop',
                'until', 'end-loop', 'restart-loop', 'for', 'while', 'in',
                'then', 'contains', 'and', 'or', 'not', 'either', 'is',
                'Otherwise',
            ), suffix=r'\b'), Keyword),

            # Keywords - other
            (words((
                'Blueprint', 'variant', 'group',
                'Return', 'EndLoop', 'RestartLoop',
                'param',
            ), suffix=r'\b'), Keyword.Declaration),

            # Built-in variant groups and types
            (words((
                'True', 'False', 'Status', 'Empty',
            ), suffix=r'\b'), Name.Builtin),

            # Type names
            (words((
                'Number', 'Text', 'List', 'Function',
            ), suffix=r'\b'), Name.Class),

            # Built-in functions
            (words((
                'print', 'len', 'push', 'pop', 'get', 'set',
                'keys', 'values', 'has', 'remove',
                'slice', 'join', 'split', 'replace',
                'upper', 'lower', 'trim',
                'map', 'filter', 'reduce', 'fold',
                'sort', 'reverse', 'find', 'contains',
                'range', 'sum', 'max', 'min',
                'type', 'str', 'int', 'float',
            ), suffix=r'\b'), Name.Builtin),

            # Numbers
            (r'-?\d+\.\d+', Number.Float),
            (r'-?\d+', Number.Integer),

            # Strings with interpolation
            (r'"', String, 'string'),

            # Function definitions - identifier : (
            (r'([a-zA-Z_\-][a-zA-Z0-9_\-]*)(\s*)(:)(\s*)(\()',
             bygroups(Name.Function, Whitespace, Operator, Whitespace, Generic.Emph), 'function-body'),

            # Function calls - identifier followed by (
            (r'([a-zA-Z_\-][a-zA-Z0-9_\-]*)(\s*)(\()',
             bygroups(Name.Function, Whitespace, Generic.Emph), 'function-args'),

            # Variable function calls - $var followed by (
            (r'(\$[a-zA-Z_\-0-9][a-zA-Z0-9_\-]*)(\s*)(\()',
             bygroups(Name.Variable, Whitespace, Name.Variable), 'function-args'),

            # Blueprint/variant group capitalized names (Person.name, Status.Ok)
            (r'[A-Z][a-zA-Z0-9_\-]*(?=\.)', Name.Class),

            # Operators - comparison and arithmetic
            (r'(\+\+|--|\*\*|<=|>=|==|!=|<|>|\+|-|\*|/|%)', Operator),
            (r'(\||&|!(?!\()|\^)', Operator),

            # Assignment operators
            (r'(=|:=|:)', Operator),

            # Punctuation
            (r'[(){}\[\];,.]', Punctuation),

            # Property access or identifiers
            (r'[a-zA-Z_\-][a-zA-Z0-9_\-]*', Name),

            # Catch-all
            (r'.', Text),
        ],
        'string': [
            # Interpolation <...>
            (r'<', Punctuation, 'interpolation'),
            # Escape sequences
            (r'\\[\\"\n]', String.Escape),
            # End of string
            (r'"', String, '#pop'),
            # String content
            (r'[^"\\<]+', String),
        ],
        'interpolation': [
            # Variable references in interpolation
            (r'@[a-zA-Z_\-][a-zA-Z0-9_\-]*', Name.Decorator),
            # Variables in interpolation
            (r'\$[a-zA-Z_\-0-9][a-zA-Z0-9_\-]*', Name.Variable),
            # End of interpolation
            (r'>', Punctuation, '#pop'),
            # Numbers in interpolation
            (r'-?\d+\.\d+', Number.Float),
            (r'-?\d+', Number.Integer),
            # Identifiers in interpolation
            (r'[a-zA-Z_\-][a-zA-Z0-9_\-]*', Name),
            # Operators
            (r'[+\-*/%]', Operator),
            # Property access
            (r'\.', Punctuation),
            # Whitespace
            (r'\s+', Whitespace),
            # Other
            (r'.', Text),
        ],
        'function-args': [
            # Closing paren - styled as function
            (r'\)', Generic.Emph, '#pop'),
            # Nested function calls
            (r'([a-zA-Z_\-][a-zA-Z0-9_\-]*)(\s*)(\()',
             bygroups(Name.Function, Whitespace, Generic.Emph), '#push'),
            # Everything else - use include to reuse root patterns
            (r'@[a-zA-Z_\-][a-zA-Z0-9_\-]*', Name.Decorator),
            (r'\$[a-zA-Z_\-0-9][a-zA-Z0-9_\-]*', Name.Variable),
            (r'-?\d+\.\d+', Number.Float),
            (r'-?\d+', Number.Integer),
            (r'"', String, 'string'),
            (r'\s+', Whitespace),
            (r'[+\-*/%<>=!&|]', Operator),
            (r'[,;.]', Punctuation),
            (r'[a-zA-Z_\-][a-zA-Z0-9_\-]*', Name),
            (r'.', Text),
        ],
        'function-body': [
            # Closing paren - styled as function
            (r'\)', Generic.Emph, '#pop'),
            # Nested function calls
            (r'([a-zA-Z_\-][a-zA-Z0-9_\-]*)(\s*)(\()',
             bygroups(Name.Function, Whitespace, Generic.Emph), '#push'),
            # Everything else
            (r'@[a-zA-Z_\-][a-zA-Z0-9_\-]*', Name.Decorator),
            (r'\$[a-zA-Z_\-0-9][a-zA-Z0-9_\-]*', Name.Variable),
            (r'-?\d+\.\d+', Number.Float),
            (r'-?\d+', Number.Integer),
            (r'"', String, 'string'),
            (r'\s+', Whitespace),
            (r'[+\-*/%<>=!&|]', Operator),
            (r'[,;.:{}]', Punctuation),
            (r'\b(?:param|return)\b', Keyword.Declaration),
            (r'[a-zA-Z_\-][a-zA-Z0-9_\-]*', Name),
            (r'.', Text),
        ],
    }
