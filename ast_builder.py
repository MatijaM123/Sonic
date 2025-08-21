# ast_builder.py
from tatsu.semantics import ModelBuilderSemantics
from typing import List

from ast_nodes import (
    FileNode,
    ImportNode,
    ParamNode,
    ExpressionNode,
    BinaryExprNode,
    FuncCallNode,
    LiteralNode,
    IdentifierNode,
    ConstDefNode,
    FuncDefNode,
    VoidCallNode,
    MainFuncNode,
)


class ASTBuilder(ModelBuilderSemantics):

    # === Root ===
    def File(self, ast):
        # ast je lista (import | funcDef | mainFunc)
        return FileNode(statements=[s for s in ast if s is not None])

    # === Imports ===
    def import_(self, ast):
        imp ,string_lit, identifier = ast
        return ImportNode(module_path=string_lit, alias=identifier)

    # === Main func ===
    def mainFunc(self, ast):
        return MainFuncNode(definitions=ast)

    # === Function definition ===
    def funcDef(self, ast):
        p1,type,identifier,p2,paramList,p3,p4,declarations,p5,ReturnExpr,dedent=ast   
        head, tail = paramList
        return FuncDefNode(
            return_type=type,
            name=identifier,
            params=(tail.insert(0,head)) or [],
            declarations=declarations,
            return_expr=ReturnExpr,
        )

    def param(self, ast):
        identifier, dd, type = ast
        return ParamNode(name=identifier, type=type)

    def paramList(self, ast):
        # već vraća listu parametara
        return ast

    # === Definitions ===
    def ConstDef(self, ast):
        identifier, eq, expression=ast
        return ConstDefNode(name=identifier, value=expression)

    def VoidCall(self, ast):
        return VoidCallNode(name=ast.identifier, args=ast.argList or [])

    # === Expressions ===
    def expression(self, ast):
        # Ako već ExpressionNode, vrati ga
        if isinstance(ast, ExpressionNode):
            return ast
        if isinstance(ast, str):
            return IdentifierNode(name=ast)
        a = ExpressionNode()
        a.value = ast
        return a

    def BinaryExpr(self, ast):
        left, op, right = ast
        return BinaryExprNode(left=left, op=op, right=right)

    def importRef(self, ast):
        mod, name = ast
        a = ExpressionNode()
        a.value = f"{mod}.{name}"
        return a

    def Literal(self, ast):
        return LiteralNode(literal=ast)

    def identifier(self, ast):
        return IdentifierNode(name=ast)

    def number(self, ast):
        return LiteralNode(literal=float(ast) if '.' in ast else int(ast), type="number")

    def stringLiteral(self, ast):
        return LiteralNode(literal=ast.strip('"'), type="string")

    def booleanLiteral(self, ast):
        return LiteralNode(literal=(ast == "true"), type="bool")

    def argList(self, ast):
        return list(ast)

    def FuncCall(self, ast):
        name, args = ast
        return FuncCallNode(name=name, arguments=args or [])
