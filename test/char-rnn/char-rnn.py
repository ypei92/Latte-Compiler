import math
import numpy as np

def load_data():
    vocab = {}
    f = open('input.txt', 'r')
    words = list(f.read())
    dataset = np.zeros(len(words), dtype = int)
    for i in range(len(words)):
        char = words[i]
        if not vocab.has_key(char):
            vocab[char] = len(vocab) + 1
        dataset[i] = vocab[char]
    print "corpus lenght : " + len(words)
    print "vocab size    : " + len(vocab)
    return dataset, words, vocab

def main():
    dataset, words, vocab = load_data()
    
    n_units = 128
    n_vocab = len(vocab)
    batch_size = 50
    bprop_len = 50

    net = Net(batch_size, 50)
    data, data_value = MemoryDataLayer(net, 'data', (1,))
    label, label_value = MemoryDataLayer(net, 'label', (1,))
    embed = EmbedIDLayer('embed', net, data, n_vocab, n_units)
    gru1 = GRUlayer('gru1', net, m embed, n_units)
    gru2 = GRUlayer('gru2', net, gru1, n_units)
    fc1 = InnerProductLayer('fc1', net, gru2, n_vocab)
    loss = SoftmaxLossLayer('loss', net, fc1, label)

    init(net)

    whole_len = dataset.size
    jump = div(whole_len, batch_size)
    n_epochs = 100

    params = SolvverParameters(
            LRPolicy.Inv(0.01, 0.0001, 0.75), \
            MomPolicy.Fixed(0.9), \
            10000, 0.0005, 1000)

    sgd = SGD(params)
    solver = sgd
    accum_loss = 0.0
    for i in range(0, n_epochs):
        loss = 0.0
        for t in range(0, 50):
            for j in range(0, batch_size):
            data_value[j] = dataset[(jump*j + 50*i + t)%whole_len + 1]
            label_value[j] = dataset[(jump*j + 50*i + t + 1)%whole_len + 1]
        forward(net, t)
        loss += get_buffer(net, 'lossvalue', t)[1]
    print "info"
    backward(net)
    solver.state.learning_rate = get_learnign_rate(solver.params.lr_policy, \
            solver.state)
    solver.state.momentum = get_momentum(solver.params.mem_policy, solver.state)
    update(solver, net)
    clear_values(net)
    clear_gd_values(net)


if __name__ == "__main__":
    main()
    

