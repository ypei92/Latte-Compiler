import sys                                                                          
sys.path.append('./stdlib')
sys.path.append('./stdlib/layers')
sys.path.append('../userdef/')

from neuron import *
from conncection import *
from ensemble import *
from network import *
from EmbedIDLayer import *
from GRULayer import *
from MemoryDataLayer import *
from FullyConnectedLayer import *
from InnerProductLayer import *
from SoftmaxLossLayer import *
from tools import *
import ast
import numpy as np

def main():
    n = Neuron()
    #top = ast.parse(neuron)
    #print ast.dump(top)

if __name__ == "__main__":
    main()
    
    

