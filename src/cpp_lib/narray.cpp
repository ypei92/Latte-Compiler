#include <vector>
#include <math.h>
#include <iostream>
#include <cstdlib>
#include <ctime>
#include <map> 

using namespace std;

float* xavier(vector<int> dim){
    int size = 1;
    float fan_in = 1.0;
    for(int i = 0; i < dim.size() - 1; ++i){
        size *= dim[i];
        fan_in *= dim[i];
    }
    size *= dim[dim.size()-1];
    float scale = sqrt(3.0/fan_in);

    float* buffer = new float[size];
    for(int i = 0; i < size; ++i){
        buffer[i] = (static_cast <float> (rand()) / static_cast <float> (RAND_MAX)) * 2 * scale - scale;
    }
    return buffer;
}

float* zeros(vector<int> dim){
    int size = 1;
    for(int i = 0; i < dim.size(); ++i){
        size *= dim[i];
    }
    float* buffer = new float[size];
    for(int i = 0; i < size; ++i){
        buffer[i] = 0.0;
    }
    return buffer;
}

map< float*, vector<int> > dim_table;
float* test_i(){
    return new float[5];
}
float* test = test_i();
vector<int> t1;
t1.push_back(3);

int main(){
    srand (static_cast <unsigned> (time(0)));

}

