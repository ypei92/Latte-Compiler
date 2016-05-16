#include <vector>
#include <math.h>
#include <iostream>
#include <fstream>
#include <cstdlib>
#include <ctime>
#include <map> 
#include <string>
#include <sys/time.h>
#include <unistd.h>

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

float max(float a , float b) {
    if (a > b)
        return a;
    else
        return b;
}

int convert_int(float a) {
    return (int) a;
}

void clear_buffer(vector<float*> buf, vector<int> size ) {
    int length = buf.size();
    if(length != size.size())
        return;

    for (int i = 0 ; i < length ; i ++) {
        for(int j = 0 ; j < size[i] ; j ++) {
            buf[i][j] = 0;
        }
    }
}

void load_data(float* a, int size, string filepath) {
    const char *cstr = filepath.c_str();
    ifstream fin(cstr);
    for (int i = 0 ; i < size ; i ++ ) {
        fin >> a[i];
    }
    fin.close();
}

long getCurrentTime()  
{  
   struct timeval tv;  
   gettimeofday(&tv,NULL);  
   return tv.tv_sec * 1000 + tv.tv_usec / 1000;  
} 

