def main():
	batch_size = 50

	datafile = '../test/fully-connected/datafile.txt'
	labelfile = '../test/fully-connected/labelfile.txt'
	
	net = Net(batch_size)
	shape = (25,)


	data = MemoryDataLayer(net, "data", shape, batch_size, datafile)
	label = MemoryDataLayer(net, "data", shape, batch_size, labelfile)
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



	
