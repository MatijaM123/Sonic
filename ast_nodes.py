from dataclasses import dataclass, field
from typing import List
from abc import ABC, abstractmethod
from context import Context
from cpp_generator import convert_type, isRef
from ast_types import *
# ===== AST ČVOROVI =====
logicOperators = ['==','!=','>','>=','<','<=']

@dataclass
class FileNode:
    statements: List
    def to_cpp(self, context: Context) -> str:
        cpp = []
        i = 0
        for statement in self.statements:
            if(not isinstance(statement,ImportNode)):
                cpp.append(statement.to_cpp(context.children[i]))
                i += 1
            else: cpp.append(statement.to_cpp(context))
        return "\n".join(cpp)

@dataclass
class ImportNode:
    module_path: str
    alias: str
    def to_cpp(self, context: Context) -> str:
        return ""

@dataclass
class ParamNode:
    name: str
    type: str
    def to_cpp(self, context: Context) -> str:
        return f"{convert_type(self.type)} {self.name}"

@dataclass
class ExpressionNode(ABC):
    @abstractmethod
    def infer_type(self, context = None) -> str:
        pass
    
@dataclass
class BinaryExprNode(ExpressionNode):
    left: ExpressionNode
    op: str
    right: ExpressionNode
    def infer_type(self,context):
        lt = self.left.infer_type(context)
        rt = self.right.infer_type(context)
        if(lt!=rt):
            raise Exception("You can't do this operation on two operands of different type!")
        if(self.op in logicOperators):
            return 'Bool'
        return lt
    def to_cpp(self, context: Context) -> str:
        return f"{self.left.to_cpp(context)}{self.op}{self.right.to_cpp(context)}"

@dataclass 
class FuncCallNode(ExpressionNode):
    name: str
    arguments: List[ExpressionNode] = field(default_factory=list)
    def infer_type(self, context):
        return context.lookup_func(self)
    def to_cpp(self, context: Context) -> str:
        return f"{self.name}({', '.join(map(lambda x: x.to_cpp(context), self.arguments))})"

@dataclass
class LiteralNode(ExpressionNode):
    literal: any
    type: str = None
    def infer_type(self, context = None):
        return self.type
    def to_cpp(self, context: Context) -> str:
        return f"{self.literal}"

@dataclass
class IdentifierNode(ExpressionNode):
    name: str
    type: str = None
    def infer_type(self,context):
        return context.lookup_var(self.name)  
    def to_cpp(self, context: Context) -> str:
        return f"{self.name}"
        
@dataclass
class ConstDefNode:
    name: str
    value: ExpressionNode
    def to_cpp(self, context: Context) -> str:
        return f"{convert_type(context.lookup_var(self.name))} {self.name} = {self.value.to_cpp(context)};"
    
@dataclass
class FuncDefNode:
    return_type: str
    name: str
    params: List[ParamNode]
    declarations: List
    return_expr: ExpressionNode
    def to_cpp(self, context: Context) -> str:
        cpp = []
        i = 0
        for declaration in self.declarations:
            if(isinstance(declaration,FuncDefNode)):
                cpp.append(declaration.to_cpp(context.children[i]))
                i += 1
            else: cpp.append(declaration.to_cpp(context))
            
        cpp.append(f"return {self.return_expr.to_cpp(context)};")
        capture = ", ".join(map(lambda x: f"{'&' if isRef(context.used_symbols[x]) else ''}{x}", context.used_symbols.keys()))   
        params =  ", ".join(map(lambda param: param.to_cpp(context), self.params))  
        body =  '\n'.join(cpp)     
        return f"auto {self.name} = [{capture}] ({params}) {{\n{body}\n}};"
    
@dataclass
class VoidCallNode:
    name: str
    args: List[ExpressionNode]
    def to_cpp(self, context: Context) -> str:
        return f"{self.name}({', '.join(map(lambda x: x.to_cpp(context), self.args))})"

    
@dataclass
class MainFuncNode:
    declarations: List
    def to_cpp(self, context: Context) -> str:
        cpp = []
        i = 0
        for statement in self.declarations:
            if(isinstance(statement,FuncDefNode)):
                cpp.append(statement.to_cpp(context.children[i]))
                i += 1
            else: cpp.append(statement.to_cpp(context))  
        cpp.append("return 0;")
        body = "\n".join(cpp)
        return f"int main(){{\n{body}\n}}"
    
@dataclass
class ParenExprNode(ExpressionNode):
    expr: ExpressionNode
    def infer_type(self,context):
        return self.expr.infer_type(context) 
    def to_cpp(self, context: Context) -> str:
        return f"({self.expr.to_cpp(context)})"