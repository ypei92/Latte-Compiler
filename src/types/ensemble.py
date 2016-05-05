#!/usr/bin/python

class Ensemble:
    def __init__(self, net, name, neurons, params, connections = []):
        self.net = net
        self.name = name
        self.neurons = neurons
        self.params = params
        self.phase = phase
        self.batch_fields = batch_fields 
        self.connections = connections
        #self.arg_dim_info
        net.ensembles.append(self)
