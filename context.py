class Context:
    def __init__(self, parent=None):
        self.symbols = {}        # ime → tip (lokalne deklaracije)
        self.used_symbols = {}   # ime → tip (korišćene spoljašnje)
        self.parent = parent     # za ugnježdene scope-ove (funkcije, blokovi...)
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
            t = self.parent.lookup_var(name)
            # ako se simbol ne nalazi u ovom contextu, ali postoji u parentu,
            # znači da je korišćen spoljašnji simbol → upisujemo ga u used_symbols
            if name not in self.used_symbols:
                self.used_symbols[name] = t
            return t
        raise Exception(f"Undeclared identifier '{name}'")

    def lookup_func_recursive(self, fcall, types):
        if (fcall.name in self.symbols 
            and self.symbols[fcall.name].paramTypes == types):
            return self.symbols[fcall.name].returnType
        
        if self.parent:
            return self.parent.lookup_func_recursive(fcall, types)
        
        raise Exception(
            f"No function with this signature: {fcall.name}{types} exists in this scope!"
        )

    def lookup_func(self, fcall):
        # generišu se tipovi parametara (unutar trenutnog konteksta) 
        # na osnovu tipova izraza argumenata
        types = [arg.infer_type(self) for arg in fcall.arguments]
        return self.lookup_func_recursive(fcall, types)
