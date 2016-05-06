#!/usr/bin/python

class Net: 
    def __init__(self, batch_size = 0, time_steps = 0):
    	self.ensembles = []
        self.batch_size = batch_size
        self.time_steps = time_steps
        self.curr_time_step = 0
        self.buffers = [[],[]]
