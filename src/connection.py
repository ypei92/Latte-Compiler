#!/usr/bin/python

class Connection:
    def __init__(self, ensemble, function = null):
        self.source = ensemble
        self.mapping = function

def add_connections(net, src, sink, mapping):
    net[net.index(src)].connections.append(Connection(sinsinkk, mapping))
	
