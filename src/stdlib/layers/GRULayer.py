#!/usr/bin/python

from neuron import *
import numpy as np
import math

def sigmoid(x):
    return 1.0 / (1.0 + math.exp(-x))

def gd_sigmoid(x):
    return 1.0 - x * x

def gd_tanh(x):
    return x * (1.0 - x)

class GRUNeuron(Neuron):
    def __init__(self, W_z, gd_W_z, U_z, gd_U_z, b_z,\
        gd_b_z, W_r, gd_W_r, U_r, gd_U_r, b_r, gd_b_r, W_h, gd_W_h, U_h,\
        gd_U_h, b_h, gd_b_h, r = 0.0, z = 0.0, hh = 0.0):

        self.W_z = W_z
        self.gd_W_z = gd_W_z
        self.U_z = U_z
        self.gd_U_z = gd_U_z
        self.b_z = b_z
        self.gd_b_z = gd_b_z

        self.W_r = W_r
        self.gd_W_r = gd_W_r
        self.U_r = U_r
        self.gd_U_r = gd_U_r
        self.b_r = b_r
        self.gd_b_r = gd_b_r

        self.W_h = W_h
        self.gd_W_h = gd_W_h
        self.U_h = U_h
        self.gd_U_h = gd_U_h
        self.b_h = b_h
        self.gd_b_h = gd_b_h

        self.r = r
        self.z = z
        self.hh = hh

    def forward(neuron):
        x_z = neuron.b_z[0]
        x_r = neuron.b_r[0]
        x_h = neuron.b_h[0]

        for i in range(size(neuron.inputs[0])):
            x_z += neuron.W_z[i] * neuron.inputs[0][i]
            x_r += neuron.W_r[i] * neuron.inputs[0][i]
            x_h += neuron.W_h[i] * neuron.inputs[0][i]

        u_z = 0.0
        u_r = 0.0
        for i in range(size(neuron.inputs[1])):
            u_z += neuron.U_z[i] * neuron.inputs[1][i]
            u_r += neuron.U_r[i] * neuron.inputs[1][i]

        neuron.z = sigmoid(x_z + u_z)
        neuron.r = sigmoid(x_r + u_r)
        u_h = 0.0
        for i in range(size(neuron.inputs[1])):
            u_h += neuron.U_h[i] * neuron.r * neuron.inputs[1][i]

        neuron.hh = tanh(x_h + u_h)
        #TODO ###################
        neuron.value = neuron.z * neuron.inputs[1][neuron.index] + (1 - neuron.z) * neuron.hh

    def backward(neuron):
        gd_z = neuron.gd_value * neuron.hh
        gd_hh = neuron.gd_value * (1 - neuron.z)
        #TODO ###################
        gd_z = gd_sigmoid(neuron.gd_value * neuron.inputs[1][neuron.index])
        neuron.gd_inputs[1][neuron.index] = neuron.gd_value * neuron.z
        gd_h = gd_tanh(gd_hh)
        gd_r = 0.0
        for i in range(size(neuron.inputs[1])):
            neuron.gd_U_h[i] += gd_h * neuron.r * neuron.inputs[1][i]
            neuron.gd_inputs[1][i] += gd_h * neuron.r * neuron.U_h[i]
            gd_r += gd_h * neuron.U_h[i] * neuron.inputs[1][i]

        gd_r = gd_sigmoid(gd_r)
        for i in range(size(neuron.inputs[1])):
            neuron.gd_U_z[i] += gd_z * neuron.inputs[1][i]
            neuron.gd_inputs[1][i] += gd_z * neuron.U_z[i]
            neuron.gd_U_r[i] += gd_r * neuron.inputs[1][i]
            neuron.gd_inputs[1][i] += gd_r * neuron.U_r[i]

        for i in range(size(neuron.inputs[1])):
            neuron.gd_W_z[i] += gd_z * neuron.inputs[0][i]
            neuron.gd_inputs[0][i] += gd_z * neuron.W_z[i]
            neuron.gd_W_r[i] += gd_r * neuron.inputs[0][i]
            neuron.gd_inputs[1][i] += gd_r * neuron.W_r[i]
            neuron.gd_W_h[i] += gd_h * neuron.inputs[0][i]
            neuron.gd_inputs[1][i] += gd_h * neuron.W_h[i]

        neuron.gd_b_h[0] = gd_h
        neuron.gd_b_r[0] = gd_r
        neuron.gd_b_z[0] = gd_z

def GRULayer(name, net, input_ensemble, num_outputs):
    
    in_out_shape = (input_ensemble.neurons.size, num_outputs)
    out_out_shape = (num_outputs, num_outputs)

    W_z = xavier(input_ensemble.neurons.size, num_outputs)
    gd_W_z = np.zeros(in_out_shape, dtype = float)

    U_z = xavier(num_outputs, num_outputs)
    gd_W_z = np.zeros(out_out_shape, dtype = float)

    b_z = np.zeros((1, num_outputs), dtype = float)
    gd_b_z = np.zeros((1, num_outputs), dtype = float)

    W_r = xavier(input_ensemble.neurons.size, num_outputs)
    gd_W_r = np.zeros(in_out_shape, dtype = float)

    U_r = xavier(num_outputs, num_outputs)
    gd_U_r = np.zeros(out_out_shape, dtype = float)

    b_r = np.zeros((1, num_outputs), dtype = float)
    gd_b_r = np.zeros((1,num_outputs), dtype = float)

    W_h = xavier(input_ensemble.neurons.size, num_outputs)
    gd_W_h = np.zeros(in_out_shape, dtype = float)

    U_h = xavier(num_outputs, num_outputs)
    gd_U_h = np.zeros(num_outputs, num_outputs)

    b_h = np.zeros((1, num_outputs), dtype = float)
    gd_b_h = np.zeros((1, num_outputs), dtype = float)

    neurons = np.empty(num_outputs, dtype = object)

    for i in range(num_outputs):
        neurons[i] = GRUNeuron(W_z[:,i], gd_W_z[:, i],\
            U_z[:,i], gd_U_z[:,i], b_z[:,i], gd_b_z[:,i], W_r[:,i], gd_W_r[:,i],\
            U_r[:,i], gd_U_r[:,i], b_r[:,i], gd_b_r[:,i], W_h[:,i], gd_W_h[:,i],\
            U_h[:,i], gd_U_h[:,i], b_h[:,i], gd_b_h[:,i])

    ens = Ensemble(net, name, neurons, [Param(net, name,"W_z", 1.0),  Param(net, name,"U_z", 1.0),\
        Param(net, name,"b_z", 2.0), Param(net, name,"W_r", 1.0), Param(net, name,"U_r", 1.0),\
        Param(net, name,"b_r", 2.0), Param(net, name,"W_h", 1.0), Param(net, name,"U_h", 1.0),\
        Param(net, name,"b_h", 2.0)])

    def mapping():
        indices = []
        for d in input_ensemble.neurons.shape:
            indices.append((0,d))
        return indices

    add_connections(net, input_ensemble, ens, mapping)
    add_connections(net, ens, ens, mapping, recurrent = true)

    return ens


