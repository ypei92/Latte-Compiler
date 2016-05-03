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
    print words 
    print vocab
    print dataset
    return words

def main():
    #dataset, words, vocab = load_data()
    words = load_data()
    
if __name__ == "__main__":
    main()
