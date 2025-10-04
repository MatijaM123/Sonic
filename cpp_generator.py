from ast_nodes import *

def generate_cpp(file, context):
    return file.to_cpp(context)



    
def convert_type(type)->str:
    return type.lower()
def isRef(type)->bool:
    return type == "String" or type == "Signal"#za sada samo string i Signal su referentni tipovi podataka, kasnije ćemo imati i nizove itd...