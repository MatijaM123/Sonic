import tatsu
from ast_builder import ASTBuilder
from util import pretty_print
def mark_indentation(src: str) -> str:
    lines = src.splitlines()
    result = []
    indent_stack = [0]

    for line in lines:
        stripped = line.lstrip("\t ")
        if not stripped:
            continue

        # Izmeri indent level (pretpostavimo tab = 1 indent ili 4 space = 1 indent)
        spaces = len(line) - len(stripped)
        indent_level = spaces // 4 + line.count("\t")

        current_indent = indent_stack[-1]

        # Ako se smanjila indentacija -> dodaj DEDENT odmah iza prethodne linije
        while indent_level < current_indent:
            result[-1] += ";DEDENT;"
            indent_stack.pop()
            current_indent = indent_stack[-1]

        # Ako je linija unutar bloka, dodaj ;INDENT; prefiks za svaku liniju
        prefix = ";INDENT;" * indent_level
        result.append(f"{prefix}{stripped}")

        # Ako linija završava sa ":" -> uvećaj indent level za sledeću liniju
        if stripped.endswith(":"):
            indent_stack.append(indent_level + 1)

    # Ako je ostalo otvorenih indentacija -> zatvori ih
    while len(indent_stack) > 1:
        result[-1] += ";DEDENT;"
        indent_stack.pop()

    return "\n"+(("\n".join(result)).replace(";INDENT;", ""))

with open('grammar.tatsu', 'r', encoding='utf-8') as f:
    grammar = f.read()

# Kompajliranje gramatike
model = tatsu.compile(grammar)

# Primer ulaznog programa

with open('source.snc', 'r',encoding='utf-8') as s:
    source = s.read()

print(mark_indentation(source))
ast = model.parse(mark_indentation(source))
pretty_print(ast)
ast = model.parse(mark_indentation(source),semantics=ASTBuilder())
pretty_print(ast)