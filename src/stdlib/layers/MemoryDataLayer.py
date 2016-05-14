#!/usr/bin/python

from neuron import*
from ensemble import*

class MemoryDataEnsemble():
    def __init__(self, name, neurons, value, phase, batch_size, net_subgroup = 1):
        self.name = name
        self.neurons = neurons
        self.value = value
        self.connections = []
        self.phase = phase
        self.batch_size = batch_size
        self.net_subgroup = 1

    def forward(loaddata, value):
        for i in range(0, len(value)):
            value[i] = loaddata[i]

    def backward():
        pass

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
    ens = MemoryDataEnsemble(name, data_neurons, value, phase, batch_size)
    add_ensemble(net, ens)
    return ens

