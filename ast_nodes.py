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
    def infer_type(self, context) -> str:
        pass     
    
@dataclass
class BinaryExprNode(ExpressionNode):
    left: ExpressionNode
    op: str
    right: ExpressionNode
    def infer_type(self, context):
        lt = self.left.infer_type(context)
        rt = self.right.infer_type(context)
        if(lt==rt):
            raise Exception("You can't do this operation on two operands of different type!")
        if(self.op in logicOperators):
            return 'Bool'
        return lt

@dataclass 
class FuncCallNode(ExpressionNode):
    name: str
    arguments: List[ExpressionNode] = field(default_factory=list)
    def infer_type(self, context):
        return super().infer_type(context)

@dataclass
class LiteralNode(ExpressionNode):
    literal: any
    type: str = None
    def infer_type(self, context):
        return self.type

@dataclass
class IdentifierNode(ExpressionNode):
    name: str
    def infer_type(self, context):
        return super().infer_type(context)
        #return context.getType(self)       
        
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
    definitions: List
    
@dataclass
class ParenExprNode(ExpressionNode):
    expr: ExpressionNode