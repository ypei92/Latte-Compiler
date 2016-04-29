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
        for i in 1:len(neuron.inputs[1]):
            neuron.value += neuron.weights[i] * neuron.inputs[1][i]
        neuron.value += neuron.bias[1]

    def backward(neuron):
        for i in 1:len(neuron.inputs[1]):
            neuron.gd_inputs[1][i] += neuron.weights[i] * neuron.gd_value
            neuron.gd_weights[i]+= neuron.inputs[1][i] * neuron.gd_value
        neuron.gd_bias[1] += neuron.gd_value


def FullyConnectedLayer(name, net, input_ensemble, size):
    num_inputs = len(input_ensemble.neuron)

    weights = xavier(num_inputs, size)
    gd_weights = zeros(num_inputs, size)

    bias = zeros(1, size)
    gd_bias = zeros(1, size)

    neurons = []

    for i in 1:size :
        neurons.append(WeightedNeuron(weights[i], gd_weights[i], bias[0][i], gd_bias[0][i]))
    ens = Ensemble(net, name, neurons, [Param(name, "weights", 1.0, 1.0),\ 
                                        Param(name, "bias", 2,0, 0.0)]) 

    def mapping:
        indices = []
        for i in 0:num_inputs :
            indices.append(i)
        return indices

    add_connections(net, input_ensemble, ens, mapping)
    return ens




        
