#!/usr/bin/python

from neuron import*
from ensemble import*

class MemoryDataEnsemble():
    def __init__(self, name, neurons, value, phase, net_subgroup = 1):
        self.name = name
        self.neurons = neurons
        self.value = value
        self.connections = []
        self.phase = phase
        self.net_subgroup = 1

    def forward(ens, data):
        data = ens.value

    def backward():
        return

def MemoryDataLayer(net, name, shape, batch_size, filename, phase = 'TrainTest'):
    data_neurons = empty(shape, dtype = object)
    length = size(data_neurons)

    for i in range(0, length):
        data_neurons[i] = DataNeuron(0.0)

    shape_array = list(shape)
    shape_array.append(batch_size)

    #value = empty(shape_array, dtype = float)
    #value = random(shape_array)
    value = load(shape_array, filename)
    ens = MemoryDataEnsemble(name, data_neurons, value, phase)
    add_ensemble(net, ens)
    return ens, value

