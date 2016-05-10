def main():
	batch_size = 50
	net = Net(batch_size)

	data, data_value = MemoryDataLayer(net, "data", (5, 10), batch_size)
	label, label_value = MemoryDataLayer(net, 'label', (5, 10), batch_size)
	fc1 = FullyConnectedLayer('fc1', net, data, 100)
	fc2 = FullyConnectedLayer('fc2', net, fc1, 10)
	loss= SoftmaxLossLayer('loss', net, fc2, label)

	lr_policy = LRPolicy.Inv(0.01, 0.0001, 0.75)
	mom_policy = MomPolicy.Fixed(0.9)
	max_epoch = 50
	regu_coef = 0.0005

	params = SolverParameters( lr_policy, mom_policy, max_epoch, regu_coef)
	sgd = SGD(params)
	solve(sgd, net)
