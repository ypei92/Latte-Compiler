def main():
	batch_size = 1

	datafile = '../test/fully-connected/datafile.txt'
	labelfile = '../test/fully-connected/labelfile.txt'
	
	net = Net(batch_size)
	shape = (9192,)
	shapelabel = (1,)
	n_epoch = 25
	update_rate = 0.0005
	layer1size = 4096
	layer2size = 4096

	data = MemoryDataLayer(net, "data", shape, batch_size, datafile)
	label = MemoryDataLayer(net, "data", shapelabel, batch_size, labelfile)
	fc1 = FullyConnectedLayer('fc1', net, data, layer1size)
	fc2 = FullyConnectedLayer('fc2', net, fc1, layer2size)
	loss= SoftmaxLossLayer('loss', net, fc2, label)

	lr_policy = LRPolicy.Inv(0.01, 0.0001, 0.75)
	mom_policy = MomPolicy.Fixed(0.9)
	max_epoch = 50
	regu_coef = 0.0005

	params = SolverParameters( lr_policy, mom_policy, max_epoch, regu_coef)
	sgd = SGD(params)
	solve(sgd, net)



	
