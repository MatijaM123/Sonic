from pprint import pprint

def ast_to_dict(node):
    if isinstance(node, list):
        return [ast_to_dict(n) for n in node]
    if hasattr(node, '__dict__'):
        return {k: ast_to_dict(v) for k, v in node.__dict__.items() if v is not None}
    return node


def pretty_print(node):
    pprint(ast_to_dict(node))
 
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

        # Ako se smanjila indentacija dodaj DEDENT odmah iza prethodne linije
        while indent_level < current_indent:
            result[-1] += ";DEDENT;"
            indent_stack.pop()
            current_indent = indent_stack[-1]

        # Ako je linija unutar bloka, dodaj ;INDENT; prefiks za svaku liniju
        prefix = ";INDENT;" * indent_level
        result.append(f"{prefix}{stripped}")

        # Ako linija završava sa ":" uvećaj indent level za sledeću liniju
        if stripped.endswith(":"):
            indent_stack.append(indent_level + 1)

    # Zatvaranje preostalih indentacija ako ih ima
    while len(indent_stack) > 1:
        result[-1] += ";DEDENT;"
        indent_stack.pop()

    return "\n"+(("\n".join(result)).replace(";INDENT;", ""))