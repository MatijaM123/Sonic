from ast_nodes import *
from ast_types import *

def generate_cpp(file, context):
    return file.to_cpp(context)



    
def convert_type(type)->str:
    return type
def isRef(type)->bool:
    return type == BasicType("String") or type == BasicType("Signal") or isinstance(type, ListType)#za sada samo string i Signal su referentni tipovi podataka, kasnije ćemo imati i nizove itd...