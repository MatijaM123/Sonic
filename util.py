def pretty_print(node, indent=0):
    pad = '  ' * indent
    if isinstance(node, list):
        print(f"{pad}[")
        for item in node:
            pretty_print(item, indent + 1)
        print(f"{pad}]")
    elif isinstance(node, tuple):
        print(f"{pad}(")
        for item in node:
            pretty_print(item, indent + 1)
        print(f"{pad})")
    elif hasattr(node, '__dict__'):
        print(f"{pad}{node.__class__.__name__}(")
        for k, v in node.__dict__.items():
            print(f"{pad}  {k}=", end="")
            pretty_print(v, indent + 2)
        print(f"{pad})")
    else:
        print(f"{pad}{repr(node)}")