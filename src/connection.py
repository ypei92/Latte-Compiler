#!/usr/bin/python

class Connection:
    def __init__(self, ensemble, function = null):
        self.source = ensemble
        self.mapping = function

def add_connections(net, src, sink, mapping):
    sink.connections.append(Connection(src, mapping))
	
