#include "solver.h"
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
float* loss_prob = zeros(10, 1, 1);
float* loss_value = zeros(1, 1, 1);
float* fc1_weights_hist = zeros(250, 100, 1);
float* fc1_bias_hist = zeros(1, 100, 1);
float* fc2_weights_hist = zeros(100, 10, 1);
float* fc2_bias_hist = zeros(1, 10, 1);
float* fc1_inputs_0 = data_value;
float* fc1_gd_inputs_0 = data_gd_value;
float* fc2_inputs_0 = fc1_value;
float* fc2_gd_inputs_0 = fc1_gd_value;
    for (i = 0 ; i < 0 ; i ++) { 
        data_value[i] = data_loaddata[i];
    }

    for (i = 0 ; i < 0 ; i ++) { 
        label_value[i] = label_loaddata[i];
    }

    for (j = 0 ; j < 100 ; j ++) { 
        for (i = 0 ; i < 250 ; i ++) { 
            fc1value[j] += fc1weights[j][i] * fc1inputs[j][i];
        }
        fc1value[j] += fc1bias[j];
    }

    for (j = 0 ; j < 10 ; j ++) { 
        for (i = 0 ; i < 100 ; i ++) { 
            fc2value[j] += fc2weights[j][i] * fc2inputs[j][i];
        }
        fc2value[j] += fc2bias[j];
    }

    loss_value[0] = 0.0;
    the_sum = 0.0;
    maxval = -100000000;
    for (i = 0 ; i < 10 ; i ++) { 
        maxval = max(maxval, fc2_value[i]);
    }
    for (i = 0 ; i < 10 ; i ++) { 
        loss_prob[i] = exp(fc2_value[i] - maxval);
        the_sum += loss_prob[i];
    }
    for (i = 0 ; i < 10 ; i ++) { 
        loss_prob[i] /= the_sum;
    }
    label_value = label_value[0];
    loss_value[0] -= log(max(loss_prob[label_value], 1e-05));

    label_value = label_value[0];
    loss_prob[label_value] -= 1;

    for (j = 0 ; j < 10 ; j ++) { 
        for (i = 0 ; i < 100 ; i ++) { 
            fc2gd_inputs[j][i] += fc2weights[j][i] * fc2gd_value[j];
        }
        for (i = 0 ; i < 100 ; i ++) { 
            fc2gd_weights[j][i] += fc2inputs[j][i] * fc2gd_value[j];
        }
        fc2gd_bias[j] += fc2gd_value[j];
    }

    for (j = 0 ; j < 100 ; j ++) { 
        for (i = 0 ; i < 250 ; i ++) { 
            fc1gd_inputs[j][i] += fc1weights[j][i] * fc1gd_value[j];
        }
        for (i = 0 ; i < 250 ; i ++) { 
            fc1gd_weights[j][i] += fc1inputs[j][i] * fc1gd_value[j];
        }
        fc1gd_bias[j] += fc1gd_value[j];
    }





int main(){
    return 0;
}