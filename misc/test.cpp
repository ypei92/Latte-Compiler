#include<iostream>
using namespace std;
/*
template<typename T, int N>
class Test{
    public:
        Test(T (&x)[N]):y(x){
        }
        T (&y)[N];
};

int main(){
    int a[3];
    a[0] = 1;
    a[1] = 2;
    a[2] = 3;
    Test<int, 3> t(a);
    cout<< t.y[0] << endl; 

    return 0;
}*/
class Test;

class Test2{
public:
    Test* x;
};

class Test{
public:
    Test(Test2& y, int z): x(z){
        y.x = this;
    }
    int x;
};

int main(){
    Test2 z;
    Test* y = new Test(z, 6);
    cout<<z.x->x<<endl;
    return 0;
}