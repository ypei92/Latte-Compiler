#!/usr/bin/python

class Ensemble:
    def __init__(self, net, name, neurons, params, connections = []):
        self.net = net
        self.name = name
        self.neurons = neurons
        self.params = params
        self.connections = connections
        net.ensembles.append(self)
