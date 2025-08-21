import tatsu
from ast_builder import ASTBuilder
from util import pretty_print, mark_indentation

with open('grammar.tatsu', 'r', encoding='utf-8') as f:
    grammar = f.read()

# Kompajliranje gramatike
model = tatsu.compile(grammar)

# Sonic program
with open('source.snc', 'r',encoding='utf-8') as s:
    source = s.read()

ast = model.parse(mark_indentation(source),semantics=ASTBuilder())
pretty_print(ast)