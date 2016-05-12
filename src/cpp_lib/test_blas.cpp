                         
#include <complex>
#include <iostream>
#define MKL_Complex16 std::complex<double>
#include "mkl.h"

#define N 5

int main()
{
        int n, inca = 1, incb = 1, i;
        std::complex<double> a[N], b[N], c;
        n = N;
        
        for( i = 0; i < n; i++ ){
                a[i] = std::complex<double>(i,i*2.0);
                b[i] = std::complex<double>(n-i,i*2.0);
        }
        zdotc(&c, &n, a, &inca, b, &incb );
        std::cout << "The complex dot product is: " << c << std::endl;
        return 0;
}
         