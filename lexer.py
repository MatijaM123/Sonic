import re

# --- LEXER ---
class LexerError(Exception):
    pass

class Token:
    def __init__(self, type_, value, line, col):
        self.type = type_
        self.value = value
        self.line = line
        self.col = col
    def __repr__(self):
        return f"Token({self.type}, {self.value}, {self.line}, {self.col})"

class Lexer:
    def __init__(self, code):
        self.code = code
        self.keywords = {'def', 'return', 'if', 'else', 'elif', 'while', 'for', 'in', 'void'}
        # Redosled važan: višekarakterski tokeni prvo
        self.token_specification = [
            ('ARROW',    r'->'),          # must come before OP and ASSIGN
            ('COMPARE',  r'(==|!=|<=|>=|<|>)'),
            ('ASSIGN',   r'='),
            ('OP',       r'[+\-*/]'),
            ('NUMBER',   r'\d+(\.\d*)?'),
            ('END',      r';'),
            ('ID',       r'[A-Za-z_][A-Za-z_0-9]*'),
            ('NEWLINE',  r'\n'),
            ('SKIP',     r'[ \t]+'),
            ('COLON',    r':'),
            ('COMMA',    r','),
            ('LPAREN',   r'\('),
            ('RPAREN',   r'\)'),
            ('LBRACE',   r'\{'),
            ('RBRACE',   r'\}'),
            ('LSQUARE',  r'\['),
            ('RSQUARE',  r'\]'),
            ('COMMENT',  r'\#.*'),
            ('UNKNOWN',  r'.'),
        ]
        self.tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in self.token_specification)

    def generate_tokens(self):
        line_num = 1
        line_start = 0
        for mo in re.finditer(self.tok_regex, self.code):
            kind = mo.lastgroup
            value = mo.group()
            column = mo.start() - line_start + 1
            if kind == 'NEWLINE':
                line_num += 1
                line_start = mo.end()
                yield Token('NEWLINE', value, line_num-1, column)
            elif kind == 'SKIP' or kind == 'COMMENT':
                pass
            elif kind == 'ID' and value in self.keywords:
                yield Token(value.upper(), value, line_num, column)
            elif kind == 'UNKNOWN':
                raise LexerError(f"Unknown token '{value}' at line {line_num} col {column}")
            else:
                yield Token(kind, value, line_num, column)
