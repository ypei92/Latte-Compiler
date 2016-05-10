def main():
    #dataset, words, vocab = load_data(sys.args[1])

    n_units = 128
    #n_vocab = len(vocab)
    n_vocab = 128
    batch_size = 50
    bprop_len = 50

    net = Net(batch_size, 50)
    data, data_value = MemoryDataLayer(net, 'data', (1,))
    label, label_value = MemoryDataLayer(net, 'label', (1,))
    embed = EmbedIDLayer('embed', net, data, n_vocab, n_units)
    gru1 = GRUlayer('gru1', net, embed, n_units)
    gru2 = GRUlayer('gru2', net, gru1, n_units)
    fc1 = InnerProductLayer('fc1', net, gru2, n_vocab)
    loss = SoftmaxLossLayer('loss', net, fc1, label)

    #whole_len = dataset.size
    #jump = whole_len/batch_size
    #n_epochs = 100

    params = SolverParameters(
            LRPolicy.Inv(0.01, 0.0001, 0.75), \
            MomPolicy.Fixed(0.9), \
            10000, 0.0005, 1000)

    sgd = SGD(params)
    solve(sgd, net) 


