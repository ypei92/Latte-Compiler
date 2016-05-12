def main():
    a = 1
    b = 2
    c = foo(a,b,'char')
    return c 

def foo( a , b, name ):
    print name
    return (a+b)*(a-b)
