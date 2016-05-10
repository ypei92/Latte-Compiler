import sys, os                                                                      
sys.path.append('./stdlib')
sys.path.append('./stdlib/layers')
sys.path.append('../userdef/')

from neuron import *
from connection import *
from ensemble import *
from network import *
from tools import *
import ast
import numpy as np

TopfileSymbolTable = {}
LayerDict = {}
EnsembleDict = {}
NeuronDict = {}

forward_func_ast = []
backward_func_ast = []

def initLayerDict():
    stdpath = "./stdlib/layers"
    usrpath = "../userdef"

    stddir = os.listdir(stdpath)
    usrdir = os.listdir(usrpath)
    for files in usrdir:
        LayerDict[files[0:-3]] = usrpath + '/' + files
    for files in stddir:
        if not LayerDict.has_key(files[0:-3]):
            LayerDict[files[0:-3]] = stdpath + '/' + files

def main():
    initLayerDict()

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
'''
    for i in ast.iter_fields(ch):
        print i
'''

class ast_visitor(ast.NodeVisitor):
    def visit_Module(self, node):
        print '0 Module: '
        for ch in ast.iter_child_nodes(node):
            if isinstance(ch, ast.FunctionDef):
                print '01FunctionDef: ', ch.name
                ast_visitor.getStatement(self, ch)
            elif isinstance(ch, ast.Assign):
                print '11Assign: '
                ast_visitor.getExpr(self, ch)
            elif isinstance(ch, ast.ClassDef):
                chch = ast_visitor.getChild(self, ch, 1)
                print '03ClassDef: ' + ch.name
                print 'Based on:', chch.id
                ast_visitor.getStatement(self, ch)
            else:
                print '00don\'t care'
                ast.NodeVisitor.generic_visit(self, ch)

    def getStatement(self, node):
        for ch in ast.iter_child_nodes(node):
            print ch
            if isinstance(ch, ast.Assign):
                print '11Assign: '
                for ch0 in ast.iter_child_nodes(ch):
                    print '    ', ch0
                ast_visitor.getExpr(self, ch)
            elif isinstance(ch, ast.Expr):
                print '12Expr: '
                ast_visitor.getExpr(self, ch)
            elif isinstance(ch, ast.Name):
                print '13Name: ', ch.id
                ast.NodeVisitor.generic_visit(self, ch)
            elif isinstance(ch, ast.FunctionDef):
                print '01FunctionDef: ', ch.name
                ast_visitor.getStatement(self, ch)
            elif isinstance(ch, ast.Assert):
                print '14Assert: '
                ast_visitor.getExpr(self, ch)
            elif isinstance(ch, ast.For):
                print '15For: '
                ast.NodeVisitor.generic_visit(self, ch)
            elif isinstance(ch, ast.If):
                print '16If: '
                #ast_visitor.getExpr(self, ch)
                #ast_visitor.getStatement(self, ch)
                #if(ch.haselse):
                #    ast_visitor.getStatement(self, ch)
                ast.NodeVisitor.generic_visit(self, ch)
            elif isinstance(ch, ast.arguments):
                print '17arguments: '
                for name in ast.iter_child_nodes(ch):
                    print '        Name: ', name.id
            elif isinstance(ch, ast.Return):
                print '18Return: '
                ast_visitor.getExpr(self, ch)
            elif isinstance(ch, ast.Call):
                print '19Call: '
                for ch0 in ast.iter_child_nodes(ch):
                    print '    ', ch0
                ast.NodeVisitor.generic_visit(self, ch)
            else:
                print '10don\'t care'
                ast.NodeVisitor.generic_visit(self, ch)
        
    def getExpr(self, node):
        for ch in ast.iter_child_nodes(node):
            print '        ', ch
            if isinstance(ch, ast.Name):
                print '        Name: ', ch.id
                ast.NodeVisitor.generic_visit(self, ch)



    def generic_visit(self, node):
        #print type(node).__name__
        ast.NodeVisitor.generic_visit(self, node)

    def getChild(self, node, num):
        counter = 0
        for ch in ast.iter_child_nodes(node):
            counter += 1
            if num == counter :
                break
        return ch

    #def visit_Name(self, node):
    #    print '    Name: ', node.id
    #    ast.NodeVisitor.generic_visit(self, node)


"""
    def visit_ClassDef(self, node):
        #print '16FunctionDef: ' + node.name
        ast.NodeVisitor.generic_visit(self, node)

    def visit_FunctionDef(self, node):
        #print 'FunctionDef: ' + node.name
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Assign(self, node):
        #print 'Assign: '
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Call(self, node):
        #print 'CallCall: '
        ast.NodeVisitor.generic_visit(self, node)

    

    def visit_Num(self, node):
        print '01Num: ', node.n
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Str(self, node):
        print '02Str: ' + node.s
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Tuple(self, node):
        print '031Tuple:'
        ast.NodeVisitor.generic_visit(self, node)  

    def visit_List(self, node):
        print '04List: '
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Dict(self, node):
        print '05Dict: '
        ast.NodeVisitor.generic_visit(self, node)

    def visit_NameConstant(self, node):
        print '06NameConstant: '
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Name(self, node):
        print '2Name: ', node.id 
        ast.NodeVisitor.generic_visit(self, node)
    
    def visit_Attribute(self, node):
        print '4Attribute: '
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Module(self, node):
        print '5Module'
        ast.NodeVisitor.generic_visit(self, node)
    


    

    def visit_arguments(self, node):
        print '7arguments: '
        ast.NodeVisitor.generic_visit(self, node)



    def visit_Expr(self, node):
        print '12Expr:'
        ast.NodeVisitor.generic_visit(self, node)

    def visit_ImportFrom(self, node):
        print '13ImportFrom: ' + node.module
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Import(self, node):
        print '14Import:'
        ast.NodeVisitor.generic_visit(self, node)

    def visit_alias(self, node):
        print '15alias: name: ', node.name 
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Param(self, node):
        print 'isParam'
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Load(self, node):
        print 'isLoad'
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Store(self, node):
        print 'isStore'
        ast.NodeVisitor.generic_visit(self, node)

    def visit_For(self, node):
        print '17For: '
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Subscript(self, node):
        print '18Subscript: '
        ast.NodeVisitor.generic_visit(self, node)

    def visit_AugAssign(self, node):
        print '19AugAssign: '
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Index(self, node):
        print '20Index: '
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Add(self, node):
        print 'isAdd: '
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Mult(self, node):
        print 'isMult: '
        ast.NodeVisitor.generic_visit(self, node)

    def visit_BinOp(self, node):
        print '21BinOp: '
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Return(self, node):
        print '22Return: '
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Slice(self, node):
        print '23Slice: '
        ast.NodeVisitor.generic_visit(self, node)

    def visit_ExtSlice(self, node):
        print '24ExtSlice: '
        ast.NodeVisitor.generic_visit(self, node)

    def visit_keyword(self, node):
        print '26keyword: '
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Assert(self, node):
        print '27Assert: '
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Compare(self, node):
        print '28Compare: '
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Eq(self, node):
        print 'isEq'
        ast.NodeVisitor.generic_visit(self, node)
"""



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
    

    

