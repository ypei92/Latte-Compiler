#include <iostream>
#include <fstream>
#include <stdio.h>      /* printf, scanf, puts, NULL */
#include <stdlib.h>     /* srand, rand */
#include <time.h>       /* time */

using namespace std;

int main(){
    srand (time(NULL));
    ofstream fout("datafile.txt");

    float a;
    for(int i = 0 ; i < 250 ; i ++){
        a = 2 * (static_cast <float> (rand()) / static_cast <float> (RAND_MAX)) - 1;
        fout << a << endl;
    }

    fout.close();
    return 0;
}