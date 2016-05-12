#!/usr/bin/python

class Connection:
    def __init__(self, ensemble, function, shape, size, is_dim_fixed, is_one_to_one, recurrent = False, copy = True):
        self.source = ensemble
        self.mapping = function
        self.recurrent = recurrent
        #dim
        self.shape = shape
        #number of connected neurons
        self.size = size
        #need to copy inputs buffers or not
        self.copy = copy
        self.is_dim_fixed = is_dim_fixed
        self.if_one_to_one = is_one_to_one


#range from src given sink
def check_dim(mapping, ):
    pass

def check_one_to_one():
    pass

def add_connections(net, src, sink, mapping, recurrent = False):
    #dimension analysis

    is_dim_fixed = check_dim()
    is_one_to_one = false
    if not all(is_dim_fixed):
        is_one_to_one = check_one_to_one()

    sink.connections.append(Connection(src, mapping, shape, size, is_dim_fixed, is_one_to_one, recurrent))
	
