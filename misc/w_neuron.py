#!/usr/bin/python

from network import *

class WeightedNeuron(Neuron):

	def __init__(self, weights, gd_weights, bias, gd_bias):
		Neuron.__init__(self)
		self.weights = weights
		self.gd_weights = gd_weights
		self.bias = bias
		self.gd_b ias = gd_bias

	def forward(w_neuron):
		pass

	def backward(w_neuron):
		pass
