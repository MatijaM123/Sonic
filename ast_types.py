from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Type:
    pass

@dataclass
class BasicType(Type):
    name: str
    def __str__(self):
        return self.name

@dataclass
class ListType(Type):
    element_type: Type
    def __str__(self):
        return f"[{self.element_type}]"

@dataclass
class FunctionType(Type):
    paramTypes: List[Type]
    returnType: Optional[Type]
    def __str__(self):
        args = ", ".join(map(str, self.paramTypes)) if self.paramTypes else ""
        ret = str(self.returnType) if self.returnType else "Void"
        return f"{{{args} -> {ret}}}"
