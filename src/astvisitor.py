import sys                                                                          
sys.path.append('./stdlib')
sys.path.append('./stdlib/layers')
sys.path.append('../userdef/')

from neuron import *
from connection import *
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

a = 1

def main():
    topfile = sys.argv[1]
    print('=' * 50)
    print('Latte Compiler: Processing ', topfile)
    print('=' * 50)
    ftop = open(topfile)
    top_expr = ftop.read()
    top_ast = ast.parse(top_expr)
    print ast_print(topfile, top_ast) 

if __name__ == "__main__":
    main()
    

    

