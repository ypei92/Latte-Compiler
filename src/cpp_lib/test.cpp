#include <iostream>
#include <vector>
using namespace std;
struct B{
    virtual ~B(){}
};

struct A : B{
    
    int a;
    A(int x){
        a = x;
    }
};

int func(B* x){
    if(A* d = dynamic_cast<A*>(x)){
        return d->a;
    } else return 0;
}

struct T1{
    int a;
};
struct T2{
    T1 b;
};

void func2(T1& t){
    t.a = 10;
}

int main(){
   float** f = new float[2][4][3];
   f[0][0][0] = 1;
   cout << f[0][0][0];
}