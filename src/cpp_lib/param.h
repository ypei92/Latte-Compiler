#include <string>

using namespace std;

class Param{
    public:
        Param(string en_name, string n, float lr, float rc){
            name = en_name + n;
            gd_name = en_name + "gd" + n;
            hist_name = en_name + n + "hist";
            learning_rate = lr;
            regu_coef = rc;
            clip_gd = -1.0;
        }
        string name;
        string gd_name;
        string hist_name;
        float learning_rate;
        float regu_coef;
        float clip_gd;

        //#TODO------------------
        float* value;
        float* gd;
        float* hist;
        int request;
};