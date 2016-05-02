#!/usr/bin/python

from neuron import *
import numpy as np

class WeightedNeuron(Neuron):
    def __init__(self, weights, gd_weights, bias, gd_bias):
       Neuron.__init__(self)
       self.weights = weights
       self.gd_weights = gd_weights
       self.bias = bias
       self.gd_bias = gd_bias

    def forward(neuron):
        for i in range(len(neuron.inputs[0])):
            neuron.value += neuron.weights[i] * neuron.inputs[0][i]
        neuron.value += neuron.bias[0]

    def backward(neuron):
        for i in range(len(neuron.inputs[0])):
            neuron.gd_inputs[0][i] += neuron.weights[i] * neuron.gd_value
            neuron.gd_weights[i]+= neuron.inputs[0][i] * neuron.gd_value
        neuron.gd_bias[0] += neuron.gd_value

def FullyConnectedEnsemble(name, net, num_inputs, num_outputs, weight_init = xavier, bias_init = 0):
    neurons = np.empty(num_outputs, dtype = object)

    weights = weight_init(num_inputs, num_outputs)
    gd_weights = np.zeros((num_inputs, num_outputs), dtype = float)

    bias = np.empty((1, num_outputs), dtype = float)
    bias.fill(bias_init)
    gd_bias = np.zeros((1,num_outputs), dtype = float)

    for i in range(num_outputs) :
        neurons[i] = WeightedNeuron(weights[:, i], gd_weights[:, i], bias[:, i], gd_bias[:, i])

    return Ensemble(net, name, neurons, [Param(name,"weights", 1.0, 1.0),\
                                  Param(name,"bias", 2.0, 0.0)])

def FullyConnectedEnsemble(net, num_inputs, num_outputs, weight_init = xavier, bias_init = 0):
    return FullyConnectedEnsemble("ensemble", net, num_inputs, num_outputs, weight_init, bias_init)

def InnerProductLayer(name, net, input_ensemble, num_outputs, weight_init = xavier, bias_init = 0):

    ip = FullyConnectedEnsemble(name, net, input_ensemble.neurons.size,\
                                num_outputs, weight_init, bias_init)
    def mapping:
        indices = []
        for d in input_ensemble.neurons.shape
            indices.append((0, d))
        return indices

    add_connections(net, input_ensemble, ip, mapping)
    return ip

def InnerProductLayer(net, input_ensemble, num_outputs, weight_init = xavier, bias_init = 0):
    return InnerProductLayer("ensemble", net, input_ensemble, num_outputs, weight_init, bias_init)    
