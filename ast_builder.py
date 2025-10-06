# ast_builder.py
from tatsu.semantics import ModelBuilderSemantics
from ast_types import *
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
    ParenExprNode,
    FunctionType,
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
        return MainFuncNode(declarations=flat)

    # === Function definition ===
    def funcDef(self, ast):
        params = []
        try:
            p1,type,identifier,p2,paramList,p3,p4,declarations,p5,ReturnExpr,dedent=ast   
        except:
            p1,type,identifier,p2,p3,p4,declarations,p5,ReturnExpr,dedent=ast   
        else: 
            head, tail = paramList
            params = [head]+[item[1] for item in tail] 
        flat = []
        for s in declarations:
            if s is None:
                continue
            if isinstance(s, list):  # <- tu hvataš višak []
                flat.extend(s)
            else:
                flat.append(s)
        return FuncDefNode(
            return_type=type,
            name=identifier.name,
            params=params,
            declarations=flat,
            return_expr=ReturnExpr,
        )

    def param(self, ast):
        identifier, dd, type = ast
        return ParamNode(name=identifier.name, type=type)

    def paramList(self, ast):
        return ast

    # === Definitions ===
    def ConstDef(self, ast):
        identifier, eq, expression=ast
        return ConstDefNode(name=identifier.name, value=expression)

    def VoidCall(self, ast):
        arguments = []
        try:
            void,identifier,p1, argList,p2 = ast
        except:
            void,identifier,p1,p2 = ast
        else:
            head, tail = argList
            arguments = [head]+[item[1] for item in tail]
          
        return VoidCallNode(name=identifier.name, args=arguments)

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
        return LiteralNode(literal=float(ast) if '.' in ast else int(ast), type=BasicType("Float") if '.' in ast else BasicType("Int"))

    def stringLiteral(self, ast):
        return LiteralNode(literal=ast.strip('"'), type=BasicType("String"))

    def booleanLiteral(self, ast):
        return LiteralNode(literal=(ast == "true"), type=BasicType("Bool"))

    def argList(self, ast):
        return ast

    def funcCall(self, ast):
        arguments = []
        try:
            identifier,p1, argList,p2 = ast
        except:
            identifier,p1,p2 = ast
        else:
            head, tail= argList
            arguments = [head]+[item[1] for item in tail]
        return FuncCallNode(name=identifier.name, arguments= arguments)
    
    def parenExpr(self,ast):
        lp,expr,rp = ast
        return ParenExprNode(expr=expr)
    
    
    
    def type(self, ast):
        return ast

    def basicType(self, ast):
        return BasicType(ast.name)

    def listType(self, ast):
        return ListType(ast.inner)

    def functionType(self, ast):
        arg_types = ast.args or []
        return_type = ast.ret
        return FunctionType(arg_types, return_type)

    def typeList(self, ast):
        list=[ast.first]
        if ast.rest: 
            for m in ast.rest: 
                list.append(m.more)
        return list  
    
    
