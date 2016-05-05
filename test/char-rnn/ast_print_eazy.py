import ast

def main():
    f = open("ast-test.py")
    expr = f.read()
    expr_ast = ast.parse(expr)
    print ast.dump(expr_ast)
    
if __name__ == "__main__":
    main()
