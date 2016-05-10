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
        net_subgroup = 1

    def forward(dim, ens, data, net, phase):
        data = ens.value

    def backward(dim, ens, data, net, phase):
        return

def MemoryDataLayer(net, name, shape, batch_size, phase = Traintest):
    data_neurons = empty(shape, dtype = object)
    length = size(data_neurons)

    for i in range(0, length):
        data_neurons[i] = DataNeuron(0.0)

    shape_array = list(shape)
    shape_array.append(batch_size)

    value = empty(shape, dtype = float)
    ens = MemoryDataEnsemble(name, data_neurons, value, phase)
    add_ensemble(net, ens)
    return ens, value

