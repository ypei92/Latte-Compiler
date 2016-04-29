#!/usr/bin/python

class SoftmaxLossNeuron:
    def __init__(self, value = 0, gd_value = 0):
        self.value = value
        self.gd_value = gd_value

class SoftmaxLossEnsemble:
    def __init__(self, name, neurons, connections, num_inputs, phase, net_subgroup):
        self.name = name
        self.neurons = neurons
        self.connections = connections
        self.num_inputs = num_inputs
        self.phase = phase
        self.net_subgroup = net_subgroup

def SoftmaxLossEnsemble(name, num_inputs):
    return SoftmaxLossEnsemble(name, [], [], num_inputs, Train, 1)

def init(ensemble, net):
    net.buffers[0] = {ensemble.name + "prob":[[0.0]*net.batch_size]*num_inputs}
    net.buffers[1] = {ensemble.name + "value":[0.0])}

def get_forward_args(ens):
    return [ens.name+"value", ens.name+"prob"]

def get_backward_args(ens):
    return [ens.name+"prob"]

def SoftmaxLossLayer(name, net, input_ensemble, label_ensemble):
    num_inputs = len(input_ensemble.neurons)
    softmax = SoftmaxLossEnsemble(name, num_inputs)
    net.ensembles.append(softmax)
    def mapping1:
        return [(0,num_inputs)]
    def mapping2:
        return [(0,0)]
    add_connections(net, input_ensemble, softmax, mapping1)
    add_connections(net, input_ensemble, softmax, mapping2)
    return softmax

def forward(loss, prob, input, label):
    loss[0] = 0.0
    for n in 0:len(input[0]) :
        maxval = float("-inf")
        for i in 0:len(input) :
            maxval = max(maxval, input[i][n])
        for i in 0:len(input) :
            prob[i][n] = exp(input[i][n] - maxval)
        the_sum = 0.0
        for i in 0:len(input) :
            the_sum += prob[i][n]
        for i in 0:len(input) :
            prob[i][n] /= the_sum

    for n in 0:len(input[0]) :
        #rounding DIFFERENCE
        label_value = int(round(label[0][n])
        loss[0] -= log(max(prob[label_value][n], sys.float_info.epsilon))
    loss[0] /= len(input[0])
    return 0

def back(prob, diff, label):
    for i in 0:len(diff):
        diff[i] = prob[i]
    for n in 0:len(diff[0]):
        label_value = int(round(label[0][n])
        diff[label_value][n] -= 1
    for i in 0:len(diff):
        

