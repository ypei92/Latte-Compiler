#!/usr/bin/python

from neuron import*
import numpy as np

class MemoryDataEnsemble(DataEnsemble):
    def __init__(self, name, neurons, value, phase, net_subgroup = 1):
        self.name = name
        #self.neurons = np.zeros((n,), dtype = DataNeuron) 
        #self.value = np.zeros((m,), dtype = float)
        self.neurons = neurons
        self.value = value
        self.connections = []
        self.phase = phase
        net_subgroup = 1

    def forward(dim, ens, data, net, phase):
        if net.time_steps > 1 :
            #data = ens.value[:,:,net.curr_time_step] //Learn the colon
            data = ens.value[:,1,net.curr_time_step] //Learn the colon
        else
            data = ens.value

    def backward(dim, ens, data, net, phase):
        return


def MemoryDataLayer(net, name, shape, phase = Traintest):
    data_neurons = np.empty(shape, dtype = DataNeuron)
    for i in range(0:np.size(data_neurons):
        data_neurons[i] = DataNeuron(0.0)
    shape_array = np.array(shape)
    shape_array.append(batch_size(net))
    if net.time_steps > 1:
        shape_array.append(net.time_steps)
    value = np.empty(shape, dtype = float)
    ens = MemoryDataEnsemble(name, data_neurons, value, phase)
    add_ensemble(net, ens)
    return ens, value



