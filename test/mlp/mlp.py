#!/usr/bin/python

net = Net(100)
data = HDF5DataLayer(net, "data/train.txt", "data/test.txt")
label = HDF5DataLayer(net, "data/train.txt", "data/test.txt")

fc1 = FullyConnectedLayer("fc1", net, data, 100)
fc2 = FullyConnectedLayer("fc2", net, fc1, 10)

loss = SoftmaxLossLayer("loss", net, fc2, label)
accuracy = AccuracyLayer("accuracy", net, fc2, label)

params = SolverParameters(
    lr_policy    = LRPolicy.Inv(0.01, 0.0001, 0.75),
    mom_policy   = MomPolicy.Fixed(0.9),
    max_epoch    = 50,
    regu_coef    = .0005,
    snapshot_dir = "mlp")
sgd = SGD(params)
solve(sgd, net)