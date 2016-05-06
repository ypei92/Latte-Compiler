import ast
from pythran import passmanager
from pythran import backend
def main():
    f = open("test.py")
    expr = f.read()
    expr_ast = ast.parse(expr)
    #print ast.dump(expr_ast)
    pm = passmanager.PassManager("tutorial_module")
    cxx = pm.dump(backend.Cxx, expr_ast)
    text_file = open("Output.cpp", "w")
    text_file.write(str(cxx))
    text_file.close()

if __name__ == '__main__':
    main()