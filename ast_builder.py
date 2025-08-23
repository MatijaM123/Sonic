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
    ParenExprNode
)


class ASTBuilder(ModelBuilderSemantics):

    def File(self, ast):
        flat = []
        for s in ast:
            if s is None:
                continue
            if isinstance(s, list):  # <- tu hvataš višak []
                flat.extend(s)
            else:
                flat.append(s)
        return FileNode(statements=flat)

    # === Imports ===
    def import_(self, ast):
        imp ,string_lit, identifier = ast
        return ImportNode(module_path=string_lit, alias=identifier)

    # === Main func ===
    def mainFunc(self, ast):
        p1,p2,definitions,p3 = ast
        flat = []
        for s in definitions:
            if s is None:
                continue
            if isinstance(s, list):  # <- tu hvataš višak []
                flat.extend(s)
            else:
                flat.append(s)
        return MainFuncNode(definitions=flat)

    # === Function definition ===
    def funcDef(self, ast):
        p1,type,identifier,p2,paramList,p3,p4,declarations,p5,ReturnExpr,dedent=ast   
        head, tail = paramList
        flat = []
        for s in declarations:
            if s is None:
                continue
            if isinstance(s, list):  # <- tu hvataš višak []
                flat.extend(s)
            else:
                flat.append(s)
        return FuncDefNode(
            return_type=type.name,
            name=identifier.name,
            params=[head]+[item[1] for item in tail],
            declarations=flat,
            return_expr=ReturnExpr,
        )

    def param(self, ast):
        identifier, dd, type = ast
        return ParamNode(name=identifier.name, type=type.name)

    def paramList(self, ast):
        return ast

    # === Definitions ===
    def ConstDef(self, ast):
        identifier, eq, expression=ast
        return ConstDefNode(name=identifier.name, value=expression)

    def VoidCall(self, ast):
        void,identifier,p1, head, tail,p2 = ast
        
        return VoidCallNode(name=identifier.name, args=[head]+[item[1] for item in tail] or [])

    # === Expressions ===
    def expression(self, ast):
        # Ako već ExpressionNode, vrati ga
        if isinstance(ast, (ExpressionNode,IdentifierNode,LiteralNode)):
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
        if isinstance(ast, LiteralNode):
            return ast
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

    def funcCall(self, ast):
        identifier,p1, head, tail,p2 = ast
        return FuncCallNode(name=identifier.name, arguments=[head]+[item[1] for item in tail] or [])
    
    def parenExpr(self,ast):
        lp,expr,rp = ast
        return ParenExprNode(expr=expr)
