#!/usr/bin/python
import math
import numpy as np

class SoftmaxLossNeuron:
    def __init__(self, value = 0.0, gd_value = 0.0):
        self.value = value
        self.gd_value = gd_value

class SoftmaxLossEnsemble:
    def __init__(self, name, num_inputs, neurons = np.empty(0, dtype = object), connections = [], phase = Train, net_subgroup = 1):
        self.name = name
        self.neurons = neurons
        self.connections = connections
        self.num_inputs = num_inputs
        self.phase = phase
        self.net_subgroup = net_subgroup

def init(ensemble, net):
    net.buffers[0] = {ensemble.name + "prob":np.empty((ensemble.num_inputs, net.batch_size), dtype = float)}
    net.buffers[1] = {ensemble.name + "value":np.empty(1, dtype = float)}

def get_forward_args(ens):
    return [ens.name+"value", ens.name+"prob"]

def get_backward_args(ens):
    return [ens.name+"prob"]

def SoftmaxLossLayer(name, net, input_ensemble, label_ensemble):
    num_inputs = len(input_ensemble.neurons)
    softmax = SoftmaxLossEnsemble(name, num_inputs)
    net.ensembles.append(softmax)
    def mapping1:
        return [(0,num_inputs)]
    def mapping2:
        return [(0,0)]
    add_connections(net, input_ensemble, softmax, mapping1)
    add_connections(net, input_ensemble, softmax, mapping2)
    return softmax

def forward(loss, prob, input, label):
    loss[0] = 0.0
    for n in range(input.shape[1]) :
        maxval = float("-inf")
        for i in range(input.shape[0]) :
            maxval = max(maxval, input[i][n])
        for i in range(input.shape[0]) :
            prob[i][n] = math.exp(input[i][n] - maxval)
        the_sum = 0.0
        for i in range(input.shape[0]) :
            the_sum += prob[i][n]
        for i in range(input.shape[0]) :
            prob[i][n] /= the_sum

    for n in range(input.shape[1]) :
        #rounding DIFFERENCE
        label_value = int(round(label[0][n])
        loss[0] -= math.log(max(prob[label_value][n], sys.float_info.epsilon))
    loss[0] /= input.shape[1]
    return 0

def backward(prob, diff, label):
    for i in range(diff.size) :
        diff[i] = prob[i]
    for n in range(diff.shape[1]) :
        label_value = int(round(label[0][n])
        diff[label_value][n] -= 1
    for i in range(diff.size) :
        diff[i] /= diff.shape[1]
    return 0
        

