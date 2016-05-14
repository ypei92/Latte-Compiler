#include <vector>
#include <math.h>
#include <iostream>
#include <cstdlib>
#include <ctime>
#include <map> 

using namespace std;

float* xavier(int d1, int d2, int d3){
    int size = d1 * d2 * d3;
    float fan_in = 1.0;
    if(d2 != 1){
        if(d3 != 1){
            fan_in = (float)(d1) * d2;
        } else {
            fan_in = (float)(d1);
        }
    }
    float scale = sqrt(3.0/fan_in);
    float* buffer = new float[size];
    for(int i = 0; i < size; ++i){
        buffer[i] = (static_cast <float> (rand()) / static_cast <float> (RAND_MAX)) * 2 * scale - scale;
    }
    return buffer;
}

float* zeros(int d1, int d2, int d3){
    int size = d1 * d2 * d3;
    float* buffer = new float[size];
    for(int i = 0; i < size; ++i){
        buffer[i] = 0.0;
    }
    return buffer;
}