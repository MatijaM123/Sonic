# ast_nodes.py

from dataclasses import dataclass, field
from typing import List, Optional, Union

# ===== AST ČVOROVI =====

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
class ExpressionNode:
    value: any = field(default=None, init=False)
    type: Optional[str] = field(default=None, init=False)
    
    
@dataclass
class BinaryExprNode(ExpressionNode):
    left: ExpressionNode
    op: str
    right: ExpressionNode
    def _post_init__(self):
        self.value = (self.left,self.op,self.right)

@dataclass 
class FuncCallNode(ExpressionNode):
    name: str
    arguments: List[ExpressionNode] = field(default_factory=list)
    def _post_init__(self):
        self.value = (self.name,self.arguments)

@dataclass
class LiteralNode:
    literal: any
    type: str = None
    def __post_init__(self):
        self.value = self.literal

@dataclass
class IdentifierNode:
    name: str
    def __post_init__(self):
        self.value = self.name
        
        
        
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