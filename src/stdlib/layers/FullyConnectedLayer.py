#!/usr/bin/python

from neuron import *

class WeightedNeuron(Neuron):
    def __init__(self, weights, gd_weights, bias, gd_bias):
	   Neuron.__init__(self)
	   self.weights = weights
	   self.gd_weights = gd_weights
	   self.bias = bias
	   self.gd_bias = gd_bias

    def forward(neuron):
	length = neuron.inputs[0]
        for i in range(0, length):
            neuron.value += neuron.weights[i] * neuron.inputs[0][i]
        neuron.value += neuron.bias[0]

    def backward(neuron):
	length = neuron.inputs[0]
        for i in range(0, length):
            neuron.gd_inputs[0][i] += neuron.weights[i] * neuron.gd_value
            neuron.gd_weights[i]+= neuron.inputs[0][i] * neuron.gd_value
        neuron.gd_bias[0] += neuron.gd_value


def FullyConnectedLayer(name, net, input_ensemble, size):
    num_inputs = len(input_ensemble.neuron)

    weights = xavier(num_inputs, size)
    gd_weights = zeros((num_inputs, size), dtype = float)

    bias = zeros((1, size), dtype = float)
    gd_bias = zeros((1, size), dtype = float)

    neurons = empty(size, dtype = object)

    for i in range(size):
        neurons[i] = WeightedNeuron(weights[:, i], gd_weights[:, i], bias[:, i], gd_bias[:, i])

    params = [Param(name, "weights", 1.0, 1.0), Param(name, "bias", 2,0, 0.0)]
    ens = Ensemble(net, name, neurons, params) 

    def mapping(x):
        indices = []
        for d in input_ensemble.neuron.shape :
            indices.append((0, d))
        return indices

    add_connections(net, input_ensemble, ens, mapping)
    return ens





        
