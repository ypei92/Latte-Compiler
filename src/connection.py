#!/usr/bin/python

class Connection:
	
	def __init__(self, ensemble, function):
		self.source = ensemble
		self.mapping = function


def add_connections(net, src, sink, mapping):
	net[net.index(sink)].connections = Connection(src, mapping)
	