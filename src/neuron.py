#!/usr/bin/python

class Neuron:
    def __init__(self, value = 0, gd_value = 0, inputs = [], gd_inputs = []):
        self.value = value 
    	self.gd_value = gd_value 
        self.inputs = inputs 
	self.gd_inputs = gd_inputs 
