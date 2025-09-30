from ast_nodes import *
from context import Context

def generate_cpp(file, context: Context):
    pass



    
def convert_type(type)->str:
    return type
def isRef(type)->bool:
    return type == "String" or type == "Signal"#za sada samo string i Signal su referentni tipovi podataka, kasnije ćemo imati i nizove itd...