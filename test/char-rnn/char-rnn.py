import math
import numpy as np

def load_data():
    vocab = {}
    f = open('input.txt', 'r')
    words = readall
    dataset = np.zeros(size(words), dtype = int32)
    for (i, word) in words:
        if !haskey(vocab,word)
            vocab[word] = size(keys(vocab)) + 1
        dataset[i] = vocab[word]
    print
    print
    return dataset, words, vocab

def main():
    dataset, words, vocab = load_data()
    
    n_units = 128
    n_vocab = size(keys(vocab))
    batch_size = 50
    bprop_len = 50

    net = Net(batch_size, 50)
    

