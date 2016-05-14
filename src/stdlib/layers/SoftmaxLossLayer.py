#!/usr/bin/python

class SoftmaxLossNeuron:
    def __init__(self, value = 0.0, gd_value = 0.0):
        self.value = value
        self.gd_value = gd_value

class SoftmaxLossEnsemble:
    def __init__(self, name, num_inputs, neurons, connections = [], phase = 'Train', net_subgroup = 1):
        self.name = name
        self.neurons = neurons
        self.connections = connections
        self.num_inputs = num_inputs
        self.phase = phase
        self.net_subgroup = net_subgroup

def SoftmaxLossLayer(name, net, input_ensemble, label_ensemble):
    num_inputs = len(input_ensemble.neurons)
    neurons = empty(0, dtype = object)
    softmax = SoftmaxLossEnsemble(name, num_inputs, neurons)
    net.ensembles.append(softmax)
    def mapping1():
        return [(0,num_inputs)]
    def mapping2():
        return [(0,0)]
    add_connections(net, input_ensemble, softmax, mapping1)
    add_connections(net, input_ensemble, softmax, mapping2)
    return softmax

# def forward(loss, prob, input, label):
#     loss[0] = 0.0
#     for n in range(0, input.shape[1]) :
#         maxval = -100000000
#         for i in range(0, input.shape[0]) :
#             maxval = max(maxval, input[i][n])
#         for i in range(0, input.shape[0]) :
#             prob[i][n] = exp(input[i][n] - maxval)
#             the_sum = 0.0
#         for i in range(0, input.shape[0]) :
#             the_sum += prob[i][n]
#         for i in range(0, input.shape[0]) :
#             prob[i][n] /= the_sum

#     for n in range(0, input.shape[1]) :
#         #rounding DIFFERENCE
#         label_value = int(round(label[0][n]))
#         loss[0] -= log(max(prob[label_value][n], 0.00001))
#         loss[0] /= input.shape[1]
#     return 0


def forward(loss, prob, input, label):
    loss[0] = 0.0
    the_sum = 0.0
    maxval = -100000000
    for i in range(0, len(input)) :
        maxval = max(maxval, input[i])
    for i in range(0, len(input)) :
        prob[i] = exp(input[i] - maxval)
        the_sum += prob[i]
    for i in range(0, len(input)) :
        prob[i] /= the_sum

    label_value = label[0]
    loss[0] -= log(max(prob[label_value], 0.00001))

# def backward(prob, diff, label):
#     for i in range(0, diff.size) :
#         diff[i] = prob[i]
#     for n in range(0, diff.shape[1]) :
#         label_value = int(round(label[0][n]))
#         diff[label_value][n] -= 1
#     for i in range(0, diff.size) :
#         diff[i] /= diff.shape[1]
#     return 0

def backward(prob, label):
    label_value = label[0]
    prob[label_value] -= 1

        

