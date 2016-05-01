#!/usr/bin/python

class Net: 
    def __init__(self, batch_size = 0):
	self.ensembles = []
        self.batch_size = batch_size
        self.buffers = [[],[]]
