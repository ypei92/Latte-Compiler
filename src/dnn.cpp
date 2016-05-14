#include "solver.h"
float* data_value = zeros(250, 1, 1);
float* data_gd_value = zeros(250, 1, 1);
float* label_value = zeros(250, 1, 1);
float* label_gd_value = zeros(250, 1, 1);
float* fc1_value = zeros(100, 1, 1);
float* fc1_gd_value = zeros(100, 1, 1);
float* fc1_weights = xavier(1, 100, 1);
float* fc1_gd_weights = zeros(1, 100, 1);
float* fc1_bias = zeros(1, 100, 1);
float* fc1_gd_bias = zeros(1, 100, 1);
float* fc2_value = zeros(10, 1, 1);
float* fc2_gd_value = zeros(10, 1, 1);
float* fc2_weights = xavier(1, 10, 1);
float* fc2_gd_weights = zeros(1, 10, 1);
float* fc2_bias = zeros(1, 10, 1);
float* fc2_gd_bias = zeros(1, 10, 1);
float* loss_prob = zeros(1, 1, 1);
float* loss_value = zeros(1, 1, 1);
float* fc1_weights_hist = zeros(1, 100, 1);
float* fc1_inputs_0 = data_value;
float* fc1_gd_inputs_0 = data_gd_value;
float* fc2_inputs_0 = fc1_value;
float* fc2_gd_inputs_0 = fc1_gd_value;
int main(){
return 0;
}