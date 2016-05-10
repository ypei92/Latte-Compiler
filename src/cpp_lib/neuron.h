#include <vector>

using namespace std;

class Neuron {
    public:
        Neuron(){
            value = 0;
            gd_value = 0;
        }
        Neuron(float v, float gd, vector<vector<float>> in, vector<vector<float> gd_in){
            value = v;
            gd_value = gd;
            inputs = in;
            gd_inputs = gd_in;
        }
        float value;
        float gd_value;
        vector<vector<float>> inputs;
        vector<vector<float>> gd_inputs;
};

class DataNeuron{
    public:
        DataNeuron(){
            value = 0;
            gd_value = 0;
        }
        DataNeuron(float v, float gd_v){
            value = v;
            gd_value = gd_v;
        }
        float value;
        float gd_value;
};
