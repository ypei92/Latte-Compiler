import math
import numpy as np

def gaussian(mean=0.0, std=1.0, *args):
    gaussian_array = np.random.random(args)
    gaussian_array = gaussian_array*std - mean
    return gaussian_array

def xavier(*args):
    prod = 1;
    for i in range(0, len(args)-1) :
        prod *= args[i];
    scale = math.sqrt(3.0/prod)
    xavier_array = np.random.random(args)
    xavier_array = 2*scale*xavier_array - scale
    return xavier_array

def batch_size(net):
    return net.batch_size

class Param:
    def __init__(self, ensemble_name, name, learning_rate, regu_coef):
        self.name = ensemble_name + name
        self.gradient_name = ensemble_name + "_gd_" + name
        self.hist_name = ensemble_name + "_hist_" + name
        self.learning_rate = learning_rate
        self.regu_coef = regu_coef
        self.clip_gradients = -1.0
        self.value = []
        self.gradiend = []
        self.hist = []
        self.request = 0


    
