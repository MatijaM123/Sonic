from pprint import pprint
from anytree import Node, RenderTree
from ast_nodes import *
from collections import namedtuple;
from context import Context

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



def clean_ast(node):
    if isinstance(node, list):
        return [clean_ast(x) for x in node if x not in ("\n", "DEDENT", "INDENT")]
    elif isinstance(node, dict):
        return {k: clean_ast(v) for k, v in node.items()}
    elif hasattr(node, "__dict__"):  # tvoji Node objekti
        for k, v in vars(node).items():
            setattr(node, k, clean_ast(v))
        return node
    else:
        return node


def make_tree(node, parent=None):
    name = node.__class__.__name__ if hasattr(node, '__class__') else repr(node)
    n = Node(name, parent=parent)
    if hasattr(node, '__dict__'):
        for attr, value in node.__dict__.items():
            if value is None:
                continue
            if isinstance(value, list):
                for v in value:
                    make_tree(v, n)
            else:
                make_tree(value, n)
    elif isinstance(node, list):
        for v in node:
            make_tree(v, n)
    return n

def pretty_print2(fnode):
    root = make_tree(fnode)
    for pre, _, node in RenderTree(root):
        try:
            print(f"{pre}{node.name}")
        except UnicodeEncodeError:
            print(f"{pre}{node.name}".encode("utf-8", errors="replace").decode("utf-8"))


def analyze_file(fnode: FileNode):
    
    def add_function_declarations_to_context(declarations, context):
        for declaration in declarations:
            if isinstance(declaration, ConstDefNode):
                context.declare(declaration.name,declaration.value.infer_type(context))
            elif isinstance(declaration, FuncDefNode):
                context.declare(declaration.name,generate_function_type(declaration))
                analyze_function(declaration,context)
            elif isinstance(declaration, VoidCallNode):
                pass
            else:
                raise Exception("What you tried to do is neither constant definition, function definition nor void call.")
    
    def analyze_main(main: MainFuncNode, context: Context):
        main_ctx = Context(parent=context)
        add_function_declarations_to_context(main.declarations,main_ctx)
        
    def analyze_function(func: FuncDefNode, context: Context):
        # kreiranje novog scope-a za funkciju
        func_ctx = Context(parent=context)

        # dodavanje parametara funkicje
        for p in func.params:
            func_ctx.declare(p.name, p.type)

        # dodavanje lokalnih konstanti(definicija)
        add_function_declarations_to_context(func.declarations, func_ctx)
        
        # provera tipa return izaza
        ret_type = func.return_expr.infer_type(func_ctx)
        if ret_type != func.return_type:
            raise Exception(f"Return type mismatch: expected {func.return_type}, got {ret_type}")
        
        return func_ctx
    
    file_ctx = Context()
    
    for stmt in fnode.statements:
        if isinstance(stmt , FuncDefNode):
            if(stmt.name == "main"):
                raise Exception("You can't name non main function main")
            file_ctx.declare(stmt.name,generate_function_type(stmt))
            analyze_function(stmt,file_ctx)
        elif isinstance(stmt, ImportNode):
            pass #treba implementirati import
        elif isinstance(stmt, MainFuncNode):
            file_ctx.declare("main", namedtuple("FuncType", ["returnType","paramTypes"]) ("Void", []))
            analyze_main(stmt, file_ctx)
    
    return file_ctx

def generate_function_type(func: FuncDefNode):
    return namedtuple("FuncType", ["returnType","paramTypes"]) (func.return_type, list(map(lambda x: x.type ,func.params)))

def print_context(ctx, indent=0):
    print("  " * indent + f"Context: {ctx.symbols} {ctx.used_symbols}")
    for child in ctx.children:
        print_context(child, indent + 1)
