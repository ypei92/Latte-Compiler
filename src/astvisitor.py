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
TypeSymbolTable = {}
LayerDict = {}
EnsembleDict = {}
NeuronDict = {}

forward_func_ast = []
backward_func_ast = []
mapping_func_ast = []
layer_func_ast = []
num_layer = 0

LayerCalling = []
cur_parsing_state = 0

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

    x = ast_visitor(0)
    x.visit(top_ast)

'''
    x.state = 1
    for layer in layer_func_ast:
        x.visit(layer)

    x.state = 2
    #for i 

    for i in ast.iter_fields(ch):
        print i
'''

class ast_visitor(ast.NodeVisitor):
    def __init__(self, state):
        #Parsing top    state = 0
        #Parsing layer  state = 1
        #Parsing forward or backward state = 2
        #self.indent = 0
        self.state = state

    def get_indent(self, indent):
        st = ''
        for i in range(indent):
            st += ' '
        return st

    def visit_Module(self, node):
        print '0 Module: '
        st = ''
        for ch in ast.iter_child_nodes(node):
            if isinstance(ch, ast.FunctionDef):
                if ch.name == 'forward':
                    print '!This forward'
                    forward_func_ast.append(ch)
                elif ch.name == 'backward':
                    print '!This backward'
                    backward_func_ast.append(ch)
                elif 'mapping' in ch.name:
                    print '!This mapping'
                    mapping_func_ast.append(ch)
                elif 'Layer' in ch.name:
                    print '!This Layer: ', ch.name
                    layer_func_ast.append(ch)         
                else:
                    indent = 4
                    chlist = ast_visitor.get_chlist(self, ch)
                    print 'FunctionDef: Name = ', ch.name
                    actual = ast_visitor.getActuals(self, chlist[0])
                    st += 'int ' + ch.name + actual + ' {\n'
                    for chch in chlist[1:]:
                        #print chch
                        st += ast_visitor.getStatement(self, chch)
                        #ast_visitor.getStatement(self, chch)
                        st += '\n'
                        # ast_visitor.get_indent(self, indent)
                    st += '}\n'
            elif isinstance(ch, ast.Assign):
                print 'Assign: getExpr'
                ast_visitor.getStatement(self, ch)
            elif isinstance(ch, ast.ClassDef):
                print 'ClassDef: ' + ch.name
                chlist = ast_visitor.get_chlist(self, ch)
                st += 'class ' + ch.name
                if isinstance(chlist[0], ast.Name):
                    print '    Based on: ', chlist[0].id
                    st += ': ' + chlist[0].id + ' {\n'
                    for chch in chlist[1:]:
                        st += ast_visitor.getStatement(self, chch)
                else:
                    st += ' {\n'
                    for chch in chlist:
                        st += ast_visitor.getStatement(self, chch)
                st += '}\n'
            else:
                print '00don\'t care'
                ast.NodeVisitor.generic_visit(self, ch)
        print st

    def get_chlist(self, node):
        chlist = []
        for ch in ast.iter_child_nodes(node):
            chlist.append(ch)
        return chlist

    def visit_FunctionDef(self, node):
        #for forward and backward
        print
        print 'FunctionDef part'
        print 'FunctionDef part'

    def getStatement(self, node):
        st = ''
        if isinstance(node, ast.Assign):
            chlist = ast_visitor.get_chlist(self, node)
            print 'Assign: childs = ', len(chlist) 
            targetstr = ast_visitor.getAssignTarget(self, chlist[0])
            valuestr = ast_visitor.getAssignValue(self, chlist[1])
            st = targetstr + ' = ' + valuestr + ';'
            return st

        elif isinstance(node, ast.AugAssign):
            chlist = ast_visitor.get_chlist(self, node)
            print 'AugAssign: childs = ', len(chlist)
            targetstr = ast_visitor.getAssignTarget(self, chlist[0])
            operatorstr = ast_visitor.getOperator(self, chlist[1])
            valuestr = ast_visitor.getAssignValue(self, chlist[2])
            st = targetstr + ' ' + operatorstr + '= ' + valuestr + ';'
            return st
        elif isinstance(node, ast.Expr):
            print 'Expr: '
            chlist = ast_visitor.get_chlist(self, node)
            st = ast_visitor.getAssignValue(self, chlist[0])
            return st + ';'
        elif isinstance(node, ast.For):
            st = ast_visitor.getFor(self, node)
            return st
        elif isinstance(node, ast.Return):
            chlist = ast_visitor.get_chlist(self, node)
            print 'Return: childs = ', len(chlist)
            st = 'return '+ ast_visitor.getAssignValue(self, chlist[0])
            # for ch in ast.iter_child_nodes(node):
            #     print '        ', ch
            return st + ';'
        elif isinstance(node, ast.FunctionDef):
            if node.name == 'forward':
                print '!This forward'
                forward_func_ast.append(node)

            elif node.name == 'backward':
                print '!This backward'
                backward_func_ast.append(node)
            elif 'mapping' in node.name:
                print '!This mapping'
                mapping_func_ast.append(node)
            elif 'Layer' in node.name:
                print '!This Layer: ', node.name
                layer_func_ast.append(node)         
            else:
                indent = 4
                chlist = ast_visitor.get_chlist(self, node)
                print 'FunctionDef: Name = ', node.name
                actual = ast_visitor.getActuals(self, chlist[0])
                st += 'int ' + node.name + actual + ' {\n'
                for ch in chlist[1:]:
                    #print chch
                    st += ast_visitor.getStatement(self, ch)
                    st += '\n'
            return st
                    # ast_visitor.get_indent(self, indent)
        # elif isinstance(ch, ast.Name):
        #     print 'Name: ', ch.id
        #     ast.NodeVisitor.generic_visit(self, ch)
        # elif isinstance(ch, ast.Assert):
        #     print 'Assert: '
        #     ast_visitor.getExpr(self, ch)
        # elif isinstance(ch, ast.If):
        #     print 'If: '
        #     #ast_visitor.getExpr(self, ch)
        #     #ast_visitor.getStatement(self, ch)
        #     #if(ch.haselse):
        #     #    ast_visitor.getStatement(self, ch)
        #     ast.NodeVisitor.generic_visit(self, ch)
        # elif isinstance(ch, ast.arguments):
        #     ast_visitor.getArgs(self, ch)
        else:
            print '10don\'t care', node
            ast.NodeVisitor.generic_visit(self, node)


    def getExpr(self, node):
        pass 
        # if isinstance(node, ast.Name):
        #     print '        Name: ', node.id
        #     ast.NodeVisitor.generic_visit(self, ch)
        # elif isinstance(ch, ast.Num):
        #     print '        Num: ', ch.n
        #     ast.NodeVisitor.generic_visit(self, ch)
        # elif isinstance(ch, ast.Tuple):
        #     print '        Tuple: ('
        #     ast_visitor.getExpr(self, ch)
        #     print '        )'
        # elif isinstance(ch, ast.Call):
        #     print '        Call: '                    
        #     ast_visitor.getCallParams(self, ch)
        # elif isinstance(ch, ast.Attribute):
        #     print '        Attr:(', ch.attr
        #     for chch in ast.iter_child_nodes(ch):
        #         if isinstance(chch, ast.Name):
        #             print '            Attrof:', chch.id
        #         elif isinstance(chch, ast.Load):
        #             print '            AttrLoad'
        #         elif isinstance(chch, ast.Store):
        #             print '            AttrStore'
        #         else:
        #             print 'unknown type in getExpr:Attr'
        #     print '                )'


    def getActuals(self, node):
        actuallist = []
        defaultlist = []
        st = '('
        print '    printing Actuals:'
        for ch in ast.iter_child_nodes(node):
            print '!!!!!!!',ch
            if isinstance(ch, ast.Name):
                print '        ActName:', ch.id
                actuallist.append(ch.id)
            elif isinstance(ch, ast.Num):
                print '        ActDefNum:', ch.n
                defaultlist.append(str(ch.n))
            elif isinstance(ch, ast.Str):
                print '        ActDefStr:', ch,stddir
                defaultlist.append(ch.s)
            else:
                print 'Unknown args'
        print
        for i in range(len(defaultlist)):
            actuallist[-1-i] += ' = ' + defaultlist[i]
        for tmpst in actuallist:
            st += tmpst + ', '
        if st[-1] == '(' :
            return '()'
        else:
            return st[0:-2] + ')'

    def getAssignTarget(self, node):
        #print '    AssignTarget:', node
        if isinstance(node, ast.Name):
            print '        TargetName: ', node.id
            st = str(node.id)
        elif isinstance(node, ast.Tuple):
            st = ast_visitor.getTuple(self, node)
        elif isinstance(node, ast.Subscript):
            st = ast_visitor.getSubscript(self, node)
        elif isinstance(node, ast.Attribute):
            st = ast_visitor.getAttribute(self, node)
        else:
            print 'Unknown getAssignTarget'
            st = ''
        return st

    def getAssignValue(self, node):
        #print '    AssignValue:', node
        st = ''
        if isinstance(node, ast.Num):
            print '        Num: ', node.n
            st = str(node.n)
        elif isinstance(node, ast.Name):
            print '        Name: ', node.id
            st = node.id
        elif isinstance(node, ast.Call):
            # for ch in ast.iter_child_nodes(node):
            #     print "            CallChildren: ", ch
            chlist = ast_visitor.get_chlist(self, node)
            st += ast_visitor.getCallName(self, chlist[0]) + '('
            for ch in chlist[1:]:
                st += ast_visitor.getCallParams(self, ch) + ', '
            if st[-1] == '(':
                return st + ')'
            else:
                return st[:-2] + ')'
        elif isinstance(node, ast.Subscript):
            st = ast_visitor.getSubscript(self, node)
        elif isinstance(node, ast.Attribute):
            st = ast_visitor.getAttribute(self, node)
        elif isinstance(node, ast.BinOp):
            print '        BinOp: '
            chlist = ast_visitor.get_chlist(self, node)
            left = ast_visitor.getAssignValue(self, chlist[0])
            operater = ast_visitor.getOperator(self, chlist[1])
            right = ast_visitor.getAssignValue(self, chlist[2])
            st = left + ' ' + operater + ' ' + right
        elif isinstance(node, ast.Tuple):
            st = ast_visitor.getTuple(self, node)
        elif isinstance(node, ast.List):
            st = ast_visitor.getList(self, node)
        else:
            st = 'Unknown Expr'
        return st

    def getOprand(self, node):
        print '    OprandValue:', node
        if isinstance(node, ast.Num):
            print '        Num: ', node.n
            st = str(node.n)
        elif isinstance(node, ast.Name):
            print '        Name: ', node.id
            st = node.id
        elif isinstance(node, ast.Call):
            chlist = ast_visitor.get_chlist(self, node)
            st += ast_visitor.getCallName(self, chlist[0]) + '('
            for ch in chlist[1:]:
                st += ast_visitor.getCallParams(self, ch) + ', '
            if st[-1] == '(':
                return st + ')'
            else:
                return st[:-2] + ')'
        elif isinstance(node, ast.Subscript):
            st = ast_visitor.getSubscript(self, node)
        elif isinstance(node, ast.Attribute):
            st = ast_visitor.getAttribute(self, node)
        elif isinstance(node, ast.BinOp):
            print '        BinOp: '
            chlist = ast_visitor.get_chlist(self, node)
            left = ast_visitor.getOprand(self, chlist[0])
            operater = ast_visitor.getOperator(self, chlist[1])
            right = ast_visitor.getOprand(self, chlist[2])
            st = left + ' ' + operater + ' ' + right
        else:
            st = 'Unknown Expr'
        return st

    def getCallName(self, node):
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Attribute):
            return ast_visitor.getAttribute(self, node)

    def getCallParams(self, node):
        st = ''
        print '    printing FuncParam:'
        if isinstance(node, ast.Name):
            print '        ParamName:', node.id
            st = node.id
        elif isinstance(node, ast.Num):
            print '        ParamNum:', node.n
            st = str(node.n)
        elif isinstance(node, ast.Str):
            print '        ParamStr:', node.s
            st = node.s
        elif isinstance(node, ast.Tuple):
            st = ast_visitor.getTuple(self, node)
        elif isinstance(node, ast.Attribute):
            st = ast_visitor.getAttribute(self, node)
        elif isinstance(node, ast.Subscript):
            st = ast_visitor.getSubscript(self, node)
        elif isinstance(node, ast.keyword):
            print '            keyword key:', node.arg
            print '            keyword value:', node.value.id
            st = node.arg + ' = ' + node.value.id
        elif isinstance(node, ast.BinOp):
            print '        BinOp: '
            chlist = ast_visitor.get_chlist(self, node)
            left = ast_visitor.getOprand(self, chlist[0])
            operater = ast_visitor.getOperator(self, chlist[1])
            right = ast_visitor.getOprand(self, chlist[2])
            st = left + ' ' + operater + ' ' + right
        elif isinstance(node, ast.Call):
            chlist = ast_visitor.get_chlist(self, node)
            st += ast_visitor.getCallName(self, chlist[0]) + '('
            for ch in chlist[1:]:
                st += ast_visitor.getCallParams(self, ch) + ', '
            if st[-1] == '(':
                return st + ')'
            else:
                return st[:-2] + ')'
        else:
            print 'Unknown Param in getCallParams'
        return st

    def getFor(self, node):
        chlist = ast_visitor.get_chlist(self, node)
        print 'For: childs = ', len(chlist)

        ob = node.target.id
        chlistRange = ast_visitor.get_chlist(self, chlist[1])
        start = ast_visitor.getCallParams(self, chlistRange[1])
        end = ast_visitor.getCallParams(self, chlistRange[2])

        print '            Target = ', ob
        print '            RangeStart = ', start
        print '            RangeEnd = ', end

        st = 'for ({} = {} ; {} < {} ; {} ++)'.format( ob, start, ob, end , ob)
        st += ' { \n'
        for ch in chlist[2:]:
            st += ast_visitor.getStatement(self, ch) + ';\n'
        return st + '}' 
    

    def getOperator(self, node):
        if isinstance(node, ast.Add):
            print '        + '
            return '+'
        elif isinstance(node, ast.Sub):
            print '        - '
            return '-'
        elif isinstance(node, ast.Mult):
            print '        * '
            return '*'
        elif isinstance(node, ast.Div):
            print '        / '
            return '/'
        else:
            print 'Unknown operater'

    def getTuple(self, node):
        tuplelist = []
        print '        TargetTuple('
        for ch in ast.iter_child_nodes(node):
            if isinstance(ch, ast.Name):
                print '            TupleName:', ch.id
                tuplelist.append(ch.id)
            elif isinstance(ch, ast.Num):
                print '            TupleNum:', ch.n
                tuplelist.append(ch.n)
            elif isinstance(ch, ast.Load):
                print '            TupleLoad'
            elif isinstance(ch, ast.Store):
                print '            TupleStore'
            else:
                print 'unknown type in getTuple'
        print '                )'
        st = str(tuplelist)
        st = '{' + st[1:-1] + '}'
        return st

    def getList(self, node):
        listlist = []
        print '        Targetlist('
        for ch in ast.iter_child_nodes(node):
            if isinstance(ch, ast.Name):
                print '            listName:', ch.id
                listlist.append(ch.id)
            elif isinstance(ch, ast.Num):
                print '            listNum:', ch.n
                listlist.append(ch.n)
            elif isinstance(ch, ast.Load):
                print '            listLoad'
            elif isinstance(ch, ast.Store):
                print '            listStore'
            else:
                print 'unknown type in getList'
        print '                )'
        st = str(listlist)
        st = '{' + st[1:-1] + '}'
        return st

    def getSubscript(self, node):
        print '        Subscript:'
        # for ch in ast.iter_child_nodes(node):
        #     print '            ', ch
        chlist = ast_visitor.get_chlist(self, node)
        if isinstance(chlist[0], ast.Subscript):
            st = ast_visitor.getSubscript(self, chlist[0])
        elif isinstance(chlist[0], ast.Attribute):
            st = ast_visitor.getAttribute(self, chlist[0])
        elif isinstance(chlist[0], ast.Name):
            print '        Name: ', chlist[0].id
            st = chlist[0].id

        index = ast_visitor.getIndex(self, chlist[1])
        #print st + '[' + index + ']'
        return st + '[' + index + ']'


    def getAttribute(self, node):
        print '        ParamAttr:(', node.attr
        for ch in ast.iter_child_nodes(node):
            if isinstance(ch, ast.Name):
                print '            Attrof:', ch.id
                st = ch.id
            elif isinstance(ch, ast.Attribute):
                st = ast_visitor.getAttribute(self, ch)
            elif isinstance(ch, ast.Load):
                print '            AttrLoad'
            elif isinstance(ch, ast.Store):
                print '            AttrStore'
            else:
                print 'unknown type in getAttr'
        print '                )'
        return st + '.' + node.attr

    def getIndex(self, node):
        print '            Index:'
        for ch in ast.iter_child_nodes(node):
            if isinstance(ch, ast.Name):
                print '            Name: ', ch.id
                return ch.id
            elif isinstance(ch, ast.Num):
                print '            Num: ', ch.n
                return str(ch.n)
            else:
                "Unknown type in getIndex"

    # def generic_visit(self, node):
    #     #print type(node).__name__
    #     ast.NodeVisitor.generic_visit(self, node)


class NetNode:
    def __init__(self):
        self.ensemble_list = []
        self.buffer_list = []
        self.task_list = []

class EnsembleNode:
    def __init__(self, name):
        self.ensemble_name = name
        self.ensemble_fields_list = []
        self.ensemble_actuals_list = []
        self.neuron_size = 0
        self.neuron_type = ''
        self.neuron_fields_list = []
        self.source_list = []
        self.forward_ast = None #body ast
        self.backward_ast = None #body ast
        self.forward_actuals_list = []
        self.backward_actuals_list = []

class FieldsNode:
    def __init__(self):
        self.name = ''
        self.type = ''
        self.init = ''

class ActualNode:
    def __init__(self):
        self.name = ''
        self.type = ''
        #self.value

class SourceNode:
    def __init__(self, ens):
        self.source_ensemble = ens
        self.mapping_ast = None
        self.is_dim_fixed = False
        self.is_one_to_one = False


if __name__ == "__main__":
    main()
    

    

