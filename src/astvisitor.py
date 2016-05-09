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

ensemble_list = []
class ensemble_node:
    def __init__():
        pass

def main():
    topfile = sys.argv[1]
    print('=' * 50)
    print('Latte Compiler: Processing ', topfile)
    print('=' * 50)
    ftop = open(topfile)
    top_expr = ftop.read()
    top_ast = ast.parse(top_expr)
    ast_print(topfile, top_ast) 

    x = ast_visitor()
    x.visit(top_ast)

class ast_visitor(ast.NodeVisitor):
    def generic_visit(self, node):
        print '1' + type(node).__name__
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Name(self, node):
        print '2Name: ', node.id 
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Call(self, node):
        print '3CallName: ', node.func.id 
        #print '3CallName: ' 
        ast.NodeVisitor.generic_visit(self, node)
    
    def visit_Attribute(self, node):
        print '4Attribute: '
        ast.NodeVisitor.generic_visit(self, node)
'''
class NetNode:
    def __init__(self, batch_size = 1 , time_step = 1):
        self.batch_size = batch_size
        self.time_step = time_step
        self.params = []
        self.ensemble_list = []
        self.train_epoch = 1
        self.test_epoch = 1
        self.curr_time_step = 0

class EnsembleNode:
    def __init__(self, name, neurons, params, connections = []):
        self.name = name
        self.params = params
        self.neuron_list = neurons
        #self.ensemble_type
        #self.forward_func_ast
        #self.backward_func_ast
        self.ensemble_source_list = []
        self.buffer_list = []

class ConnectionNode:
    def __init__(self, ensemble, function, recurrent = False):
        self.source = ensemble
        self.mapping = function
        self.recurrent = recurrent
        self.size = 0
        self.copy = True
        self.is_dim_fixed = []
        self.if_one_to_one = True

class NeuronNode:
    def __init__(self, name):
        self.name = name
        self.field_list = []
'''

if __name__ == "__main__":
    main()
    

    

