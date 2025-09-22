from dataclasses import dataclass, field
from typing import List, Optional
from abc import ABC, abstractmethod


# ===== AST ČVOROVI =====
logicOperators = ['==','!=','>','>=','<','<=']

@dataclass
class FileNode:
    statements: List

@dataclass
class ImportNode:
    module_path: str
    alias: str

@dataclass
class ParamNode:
    name: str
    type: str

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

@dataclass 
class FuncCallNode(ExpressionNode):
    name: str
    arguments: List[ExpressionNode] = field(default_factory=list)
    def infer_type(self, context):
        return context.lookup_func(self)

@dataclass
class LiteralNode(ExpressionNode):
    literal: any
    type: str = None
    def infer_type(self, context = None):
        return self.type

@dataclass
class IdentifierNode(ExpressionNode):
    name: str
    type: str = None
    def infer_type(self,context):
        return context.lookup_var(self.name)  
        
@dataclass
class ConstDefNode:
    name: str
    value: ExpressionNode
    
@dataclass
class FuncDefNode:
    return_type: str
    name: str
    params: List[ParamNode]
    declarations: List
    return_expr: ExpressionNode
    
@dataclass
class VoidCallNode:
    name: str
    args: List[ExpressionNode]
    
@dataclass
class MainFuncNode:
    declarations: List
    
@dataclass
class ParenExprNode(ExpressionNode):
    expr: ExpressionNode
    def infer_type(self,context):
        return self.expr.infer_type(context) 
class Context:
    def __init__(self, parent=None):
        self.symbols = {}      # ime → tip
        self.parent = parent   # za ugnježdene scope-ove (funkcije, blokovi...)
        self.children = []
        
        if parent:
            parent.children.append(self)

    def declare(self, name, type_):
        if name in self.symbols:
            raise Exception(f"Redefinition of '{name}'")
        
        self.symbols[name] = type_

    def lookup_var(self, name):
        if name in self.symbols:
            return self.symbols[name]
        if self.parent:
            return self.parent.lookup_var(name)
        raise Exception(f"Undeclared identifier '{name}'")
    
    def lookup_func_recursive(self, fcall: FuncCallNode, types):
        if(fcall.name in self.symbols and self.symbols[fcall.name].paramTypes == types):
            return self.symbols[fcall.name].returnType
        if  self.parent:
            return self.parent.lookup_func_recursive(fcall,types)
        raise Exception(f"No function with this signature: {fcall.name}{types} exists in this scope!")
        #poželjno malo optimizovati
    
    
    def lookup_func(self, fcall: FuncCallNode): #generišu se tipovi parametara (unutar trenutnog konteksta) na osnovu tipova izraza argumenata i onda se rekurzivno traži odgovarajuća funkcija kroz trenutni kontekst i kontekste koji sadrže njega
        types = list(map(lambda x: x.infer_type(self),fcall.arguments))
        return self.lookup_func_recursive(fcall,types)        
        
        
    