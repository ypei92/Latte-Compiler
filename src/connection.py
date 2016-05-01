#!/usr/bin/python

class Connection:
    def __init__(self, ensemble, function = null, recurrent = false):
        self.source = ensemble
        self.mapping = function
        self.recurrent = recurrent

def add_connections(net, src, sink, mapping, recurrent = false):
    sink.connections.append(Connection(src, mapping, recurrent))
	
