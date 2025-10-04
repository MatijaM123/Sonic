import tatsu
from ast_builder import ASTBuilder
from util import *
from cpp_generator import generate_cpp

with open('grammar.tatsu', 'r', encoding='utf-8') as f:
    grammar = f.read()

# Kompajliranje gramatike
model = tatsu.compile(grammar)

# Sonic program
with open('source.snc', 'r',encoding='utf-8') as s:
    source = s.read()

ast = model.parse(mark_indentation(source),semantics=ASTBuilder())
print(clean_ast(ast))
pretty_print(clean_ast(ast))
context = analyze_file(ast)
print_context(context)


print_cpp(generate_cpp(ast, context))
