#include "solver.h"
int i = 0, j = 0;
float* data_loaddata = new float[250];
float* label_loaddata = new float[1];
float* data_value = zeros(250, 1, 1);
float* data_gd_value = zeros(250, 1, 1);
float* label_value = zeros(1, 1, 1);
float* label_gd_value = zeros(1, 1, 1);
float* fc1_value = zeros(100, 1, 1);
float* fc1_gd_value = zeros(100, 1, 1);
float* fc1_weights = xavier(250, 100, 1);
float* fc1_gd_weights = zeros(250, 100, 1);
float* fc1_bias = zeros(1, 100, 1);
float* fc1_gd_bias = zeros(1, 100, 1);
float* fc2_value = zeros(10, 1, 1);
float* fc2_gd_value = zeros(10, 1, 1);
float* fc2_weights = xavier(100, 10, 1);
float* fc2_gd_weights = zeros(100, 10, 1);
float* fc2_bias = zeros(1, 10, 1);
float* fc2_gd_bias = zeros(1, 10, 1);
float* loss_value = zeros(1, 1, 1);
float* fc1_inputs_0 = data_value;
float* fc1_gd_inputs_0 = data_gd_value;
float* fc2_inputs_0 = fc1_value;
float* fc2_gd_inputs_0 = fc1_gd_value;
float* loss_prob_0 = fc2_gd_value;
float* loss_prob_1 = label_gd_value;


void forward() {
    for (i = 0 ; i < 250 ; i ++) { 
        data_value[i] = data_loaddata[i];
    }

    for (i = 0 ; i < 1 ; i ++) { 
        label_value[i] = label_loaddata[i];
    }

    for (j = 0 ; j < 100 ; j ++) { 
        for (i = 0 ; i < 250 ; i ++) { 
            fc1_value[j] += fc1_weights[j*250 + i] * fc1_inputs_0[i];
        }
        fc1_value[j] += fc1_bias[j];
    }

    for (j = 0 ; j < 10 ; j ++) { 
        for (i = 0 ; i < 100 ; i ++) { 
            fc2_value[j] += fc2_weights[j*100 + i] * fc2_inputs_0[i];
        }
        fc2_value[j] += fc2_bias[j];
    }

    float the_sum = 0.0;
    float max_val = -100000000;
    for (i = 0 ; i < 10 ; i ++) { 
        max_val = max(max_val, fc2_value[i]);
        printf("%f\n", fc2_value[i]);
    }
    for (i = 0 ; i < 10 ; i ++) { 
        loss_prob_0[i] = exp(fc2_value[i] - max_val);
        the_sum += loss_prob_0[i];
    }
    for (i = 0 ; i < 10 ; i ++) { 
        loss_prob_0[i] /= the_sum;
    }
    int target_label = convert_int(label_value[0]);
    loss_value[0] -= log(max(loss_prob_0[target_label], 1e-05));

}

void backward() {
    int target_label = convert_int(label_value[0]);
    loss_prob_0[target_label] -= 1;

    for (j = 0 ; j < 10 ; j ++) { 
        for (i = 0 ; i < 100 ; i ++) { 
            fc2_gd_inputs_0[i] += fc2_weights[j*100 + i] * fc2_gd_value[j];
        }
        for (i = 0 ; i < 100 ; i ++) { 
            fc2_gd_weights[j*100 + i] += fc2_inputs_0[i] * fc2_gd_value[j];
        }
        fc2_gd_bias[j] += fc2_gd_value[j];
    }

    for (j = 0 ; j < 100 ; j ++) { 
        for (i = 0 ; i < 250 ; i ++) { 
            fc1_gd_inputs_0[i] += fc1_weights[j*250 + i] * fc1_gd_value[j];
        }
        for (i = 0 ; i < 250 ; i ++) { 
            fc1_gd_weights[j*250 + i] += fc1_inputs_0[i] * fc1_gd_value[j];
        }
        fc1_gd_bias[j] += fc1_gd_value[j];
    }





}

void update() {
    for(i = 0; i < 100; ++i){
        for(j = 0; j < 250; ++j){
            fc1_weights[i * 250 + j] += fc1_gd_weights[i * 250 + j];
        }
    }
    for(i = 0; i < 100; ++i){
        for(j = 0; j < 1; ++j){
            fc1_bias[i * 1 + j] += fc1_gd_bias[i * 1 + j];
        }
    }
    for(i = 0; i < 10; ++i){
        for(j = 0; j < 100; ++j){
            fc2_weights[i * 100 + j] += fc2_gd_weights[i * 100 + j];
        }
    }
    for(i = 0; i < 10; ++i){
        for(j = 0; j < 1; ++j){
            fc2_bias[i * 1 + j] += fc2_gd_bias[i * 1 + j];
        }
    }
}


int main(){
    string s0 = "../test/fully-connected/datafile.txt";
    string s1 = "../test/fully-connected/labelfile.txt";
    load_data(data_loaddata, 250, s0);
    load_data(label_loaddata, 1, s1);

    vector<float*> buff;
    vector<int> dim;

    buff.push_back(data_value);
    dim.push_back(250);
    buff.push_back(data_gd_value);
    dim.push_back(250);
    buff.push_back(label_value);
    dim.push_back(1);
    buff.push_back(label_gd_value);
    dim.push_back(1);
    buff.push_back(fc1_value);
    dim.push_back(100);
    buff.push_back(fc1_gd_value);
    dim.push_back(100);
    buff.push_back(fc1_gd_weights);
    dim.push_back(25000);
    buff.push_back(fc1_gd_bias);
    dim.push_back(100);
    buff.push_back(fc2_value);
    dim.push_back(10);
    buff.push_back(fc2_gd_value);
    dim.push_back(10);
    buff.push_back(fc2_gd_weights);
    dim.push_back(1000);
    buff.push_back(fc2_gd_bias);
    dim.push_back(10);
    buff.push_back(loss_value);
    dim.push_back(1);

    for ( int k = 0 ; k < 2 ; k ++ ) {
        forward();
        printf("loss_value = %f\n", loss_value[0]);
        backward();
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