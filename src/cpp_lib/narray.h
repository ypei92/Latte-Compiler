#include <vector>
#include <math.h>
#include <iostream>

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
        buffer[i] = (static_cast <float> (rand()) / static_cast <float> (RAND_MAX)) - 2 * scale - scale;
        cout<< buffer[i] <<endl;
    }
    return buffer;
}

int main(){
    vector<int> dim;
    dim.push_back(3);
    dim.push_back(2);
    xavier(dim);
}

