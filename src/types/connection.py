#!/usr/bin/python

class Connection:
    def __init__(self, ensemble, function = null, recurrent = false):
        self.source = ensemble
        self.mapping = function
        self.recurrent = recurrent
        self.shape = ()
        self.size = 0
        self.copy = false
        self.is_dim_fixed = []
        self.if_one_to_one = true
        padding = 0

def add_connections(net, src, sink, mapping, recurrent = false):
    sink.connections.append(Connection(src, mapping, recurrent))
	
