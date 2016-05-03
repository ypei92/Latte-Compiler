#!/usr/bin/python

from neuron import *
import numpy as np

class EmbedNeuron(Neuron):
    def __init__(self, weights, gd_weights):
    Neuron.__init__(self)
    self.weights = weights
    self.gd_weights = gd_weights

    def forward(neuron):
        idx = int(round(neuron.inputs[0][0]))    
        neuron.value = neuron.weights[idx]

    def backward(neuron):
        _idx = int(round(neuron.inputs[0][0]))
        neuron.gd_weights[_idx] += neuron.gd_value

def EmbedIDLayer(name, net, input_ensemble, in_size, out_size):
    assert(input_ensemble.neurons.size == 1)
    weights = xavier(in_size, out_size)
    gd_weights = np.zeros((in_size, out_size), dtype = float)

    neurons = np.empty(1, dtype = object)

    for i in range(out_size) : 
        neurons[i] = EmbedNeuron(weights[:, i], gd_weights[:, i])

    ens = Ensemble(net, name, neurons, [Param(name, "weights", 1.0, 1.0)])

    def mapping:
        return [(0,0)]
        
    add_connections(net, input_ensemble, ens, mapping)

    return ens