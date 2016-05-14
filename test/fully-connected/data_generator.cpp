#include <iostream>
#include <fstream>
#include <stdio.h>      /* printf, scanf, puts, NULL */
#include <stdlib.h>     /* srand, rand */
#include <time.h>       /* time */

using namespace std;

int main(){
    srand (time(NULL));
    ofstream fout("datafile.txt");

    int a;
    for(int i = 0 ; i < 250 ; i ++){
        a = rand()%10;
        fout << a << endl;
    }

    fout.close();
    return 0;
}