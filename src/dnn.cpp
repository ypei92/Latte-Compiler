#include "solver.h"
#include "omp.h"
float* data_loaddata = new float[9192];
float* label_loaddata = new float[1];
float* data_value = zeros(9192, 1, 1);
float* data_gd_value = zeros(9192, 1, 1);
float* label_value = zeros(1, 1, 1);
float* label_gd_value = zeros(1, 1, 1);
float* fc1_value = zeros(4096, 1, 1);
float* fc1_gd_value = zeros(4096, 1, 1);
float* fc1_weights = xavier(9192, 4096, 1);
float* fc1_gd_weights = zeros(9192, 4096, 1);
float* fc1_bias = zeros(1, 4096, 1);
float* fc1_gd_bias = zeros(1, 4096, 1);
float* fc2_value = zeros(2048, 1, 1);
float* fc2_gd_value = zeros(2048, 1, 1);
float* fc2_weights = xavier(4096, 2048, 1);
float* fc2_gd_weights = zeros(4096, 2048, 1);
float* fc2_bias = zeros(1, 2048, 1);
float* fc2_gd_bias = zeros(1, 2048, 1);
float* loss_value = zeros(1, 1, 1);
float* fc1_inputs_0 = data_value;
float* fc1_gd_inputs_0 = data_gd_value;
float* fc2_inputs_0 = fc1_value;
float* fc2_gd_inputs_0 = fc1_gd_value;
float* loss_prob_0 = fc2_gd_value;
float* loss_prob_1 = label_gd_value;


void forward() {
    int i, j;
    for (i = 0 ; i < 9192 ; i ++) { 
        data_value[i] = data_loaddata[i];
    }

    for (i = 0 ; i < 1 ; i ++) { 
        label_value[i] = label_loaddata[i];
    }

    for (j = 0 ; j < 4096 ; j ++) { 
        for (i = 0 ; i < 9192 ; i ++) { 
            fc1_value[j] += fc1_weights[j*9192 + i] * fc1_inputs_0[i];
        }
        fc1_value[j] += fc1_bias[j];
    }
    for (j = 0 ; j < 2048 ; j ++) { 
        for (i = 0 ; i < 4096 ; i ++) { 
            fc2_value[j] += fc2_weights[j*4096 + i] * fc2_inputs_0[i];
        }
        fc2_value[j] += fc2_bias[j];
    }

    float the_sum = 0.0;
    float max_val = -100000000;
    for (i = 0 ; i < 2048 ; i ++) { 
        max_val = max(max_val, fc2_value[i]);
    }
    for (i = 0 ; i < 2048 ; i ++) { 
        loss_prob_0[i] = exp(fc2_value[i] - max_val);
        the_sum += loss_prob_0[i];
    }
    for (i = 0 ; i < 2048 ; i ++) { 
        loss_prob_0[i] /= the_sum;
    }
    int target_label = convert_int(label_value[0]);
    loss_value[0] -= log(max(loss_prob_0[target_label], 1e-05));

}

void backward() {
    int i, j;
    int target_label = convert_int(label_value[0]);
    loss_prob_0[target_label] -= 1;
    #pragma omp for
    for (j = 0 ; j < 2048 ; j ++) {  
        for (i = 0 ; i < 4096 ; i ++) { 
            fc2_gd_inputs_0[i] += fc2_weights[j*4096 + i] * fc2_gd_value[j];
            fc2_gd_weights[j*4096 + i] += fc2_inputs_0[i] * fc2_gd_value[j];
        }
        fc2_gd_bias[j] += fc2_gd_value[j];
    }
    #pragma omp for
    for (j = 0 ; j < 4096 ; j ++) { 
        for (i = 0 ; i < 9192 ; i ++) { 
            fc1_gd_inputs_0[i] += fc1_weights[j*9192 + i] * fc1_gd_value[j];
            fc1_gd_weights[j*9192 + i] += fc1_inputs_0[i] * fc1_gd_value[j];
        }
        fc1_gd_bias[j] += fc1_gd_value[j];
    }

}

void update() {
    int i, j;
    #pragma omp for
    for(i = 0; i < 4096; ++i){
        for(j = 0; j < 9192; ++j){
            fc1_weights[i * 9192 + j] -= 0.0005*fc1_gd_weights[i * 9192 + j];
        }
        fc1_bias[i] -= 0.0005*fc1_gd_bias[i];
    }
    #pragma omp for
    for(i = 0; i < 2048; ++i){
        for(j = 0; j < 4096; ++j){
            fc2_weights[i * 4096 + j] -= 0.0005*fc2_gd_weights[i * 4096 + j];
        }
        fc2_bias[i] -= 0.0005*fc2_gd_bias[i];
    }
}


int main(){
    string s0 = "../test/fully-connected/datafile.txt";
    string s1 = "../test/fully-connected/labelfile.txt";
    load_data(data_loaddata, 9192, s0);
    load_data(label_loaddata, 1, s1);

    vector<float*> buff;
    vector<int> dim;

    buff.push_back(data_value);
    dim.push_back(9192);
    buff.push_back(data_gd_value);
    dim.push_back(9192);
    buff.push_back(label_value);
    dim.push_back(1);
    buff.push_back(label_gd_value);
    dim.push_back(1);
    buff.push_back(fc1_value);
    dim.push_back(4096);
    buff.push_back(fc1_gd_value);
    dim.push_back(4096);
    buff.push_back(fc1_gd_weights);
    dim.push_back(37650432);
    buff.push_back(fc1_gd_bias);
    dim.push_back(4096);
    buff.push_back(fc2_value);
    dim.push_back(2048);
    buff.push_back(fc2_gd_value);
    dim.push_back(2048);
    buff.push_back(fc2_gd_weights);
    dim.push_back(8388608);
    buff.push_back(fc2_gd_bias);
    dim.push_back(2048);
    buff.push_back(loss_value);
    dim.push_back(1);

    long start, end;
    for ( int k = 0 ; k < 25 ; k ++ ) {
        start = getCurrentTime();
        forward();
        backward();
        end = getCurrentTime();
        printf(" label_prob = %f\t", loss_prob_0[convert_int(label_value[0])]);
        printf(" loss = %f\t", loss_value[0]);
        printf(" Running time = %ld\n", end - start);
        update();
        clear_buffer(buff, dim);
    }

    delete []data_value;
    delete []data_gd_value;
    delete []label_value;
    delete []label_gd_value;
    delete []fc1_value;
    delete []fc1_gd_value;
    delete []fc1_weights;
    delete []fc1_gd_weights;
    delete []fc1_bias;
    delete []fc1_gd_bias;
    delete []fc2_value;
    delete []fc2_gd_value;
    delete []fc2_weights;
    delete []fc2_gd_weights;
    delete []fc2_bias;
    delete []fc2_gd_bias;
    delete []loss_value;
    delete []data_loaddata;
    delete []label_loaddata;
    return 0;
}