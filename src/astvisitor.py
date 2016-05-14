import sys, os, pprint                                                                 
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
import sets as Set
from collections import OrderedDict


TopfileSymbolTable = {}
LayerDict = {}
LayerNameList = []
LayerTypeList = []
EnsembleDict = {}
NeuronDict = {}

forward_func_ast = []
backward_func_ast = []
forward_func_actuals =[]
backward_func_actuals =[]
shared_buffer_list = []
allocated_buffer_list = []

load_buffer_list = []
load_buffer_list_size = []
load_data_path = []

output_buffer = []
output_buffer_size = []

mapping_func_ast = []


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

class ast_visitor(ast.NodeVisitor):
    def __init__(self):
        #Parsing top    state = 0
        #Parsing layer  state = 1
        #Parsing forward or backward state = 2
        self.state = 0
        self.indent = 0

    def get_indent(self):
        st = ''
        for i in range(self.indent):
            st += ' '
        return st

    def visit_Module(self, node):
        # print '0 Module: '
        st = ''
        if self.state == 0:
            for ch in ast.iter_child_nodes(node):
                if isinstance(ch, ast.FunctionDef):
                    if ch.name == 'forward':
                        # print '!This forward'
                        forward_func_ast.append(ch)
                    elif ch.name == 'backward':
                        # print '!This backward'
                        backward_func_ast.append(ch)
                    elif 'mapping' in ch.name:
                        # print '!This mapping'
                        mapping_func_ast.append(ch)       
                    else:
                        self.indent += 4
                        chlist = ast_visitor.get_chlist(self, ch)
                        print 'FunctionDef: Name = ', ch.name
                        actual, actuallist = ast_visitor.getActuals(self, chlist[0])
                        st += 'int ' + ch.name + actual + ' {\n'
                        for chch in chlist[1:]:
                            #print chch
                            st += ast_visitor.getStatement(self, chch)
                            #ast_visitor.getStatement(self, chch)
                            st += '\n'
                            # ast_visitor.self.get_indent(self, indent)
                        st += '}\n'
                        self.indent -= 4
                elif isinstance(ch, ast.Assign):
                    # print 'Assign: getExpr'
                    ast_visitor.getStatement(self, ch)
                elif isinstance(ch, ast.ClassDef):
                    print 'ClassDef: ' + ch.name
                    self.indent += 4
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
                    self.indent -= 4
                else:
                    print '00don\'t care'
                    ast.NodeVisitor.generic_visit(self, ch)
            print st

        elif self.state == 1:
            for ch in ast.iter_child_nodes(node):
                if isinstance(ch , ast.ClassDef):
                    print 'ClassDef: ' + ch.name
                    chlist = ast_visitor.get_chlist(self, ch)
                    for chch in chlist:
                        st = ast_visitor.getFunctionDef(self, chch)
                        if st == 'forward':
                            forward_func_ast.append(chch)
                            chlist0 = ast_visitor.get_chlist(self, chch)
                            st0 , actuallist = ast_visitor.getActuals(self, chlist0[0])
                            forward_func_actuals.append(actuallist)
                        elif st == 'backward':
                            backward_func_ast.append(chch)
                            chlist0 = ast_visitor.get_chlist(self, chch)
                            st0 , actuallist = ast_visitor.getActuals(self, chlist0[0])
                            backward_func_actuals.append(actuallist)
                elif isinstance(ch, ast.FunctionDef):
                    #print ch.name
                    if ch.name == 'forward':
                        forward_func_ast.append(ch)
                        chlist0 = ast_visitor.get_chlist(self, ch)
                        st0 , actuallist = ast_visitor.getActuals(self, chlist0[0])
                        forward_func_actuals.append(actuallist)
                    elif ch.name == 'backward':
                        backward_func_ast.append(ch)
                        chlist0 = ast_visitor.get_chlist(self, ch)
                        st0 , actuallist = ast_visitor.getActuals(self, chlist0[0])
                        backward_func_actuals.append(actuallist)



    def get_chlist(self, node):
        chlist = []
        for ch in ast.iter_child_nodes(node):
            chlist.append(ch)
        return chlist

    def visit_FunctionDef(self, node):
        #for forward and backward
        if self.state ==2 :
            # print
            # print 'FunctionDef part'
            # node.name = '123'
            # for ch in ast.iter_child_nodes(node):
            #     print 'Children of FunctionDef:', ch
            # print
            self.indent += 4
            st = ''
            chlist = ast_visitor.get_chlist(self, node)
            for ch in chlist[1:]:
                st += ast_visitor.getStatement(self, ch)
                #ast_visitor.getStatement(self, chch)
                st += '\n'
            self.indent -= 4
            output_file.write(st)
            output_file.write('\n')
        else:
            print "stateError"


    def getStatement(self, node):
        st = ''
        if isinstance(node, ast.Assign):
            chlist = ast_visitor.get_chlist(self, node)
            # print 'Assign: childs = ', len(chlist) 
            targetstr, targetname = ast_visitor.getAssignTarget(self, chlist[0])
            valuestr, valuelist = ast_visitor.getAssignValue(self, chlist[1]) 
            
            if self.state == 0:
                st = self.get_indent() + targetstr + ' = ' + valuestr + ';'
                TopfileSymbolTable[targetname] = valuelist
                if 'Layer' in st:
                    LayerNameList.append(targetname)

            if self.state == 2:
                if targetstr == 'the_sum':
                    targetstr = 'float ' + targetstr
                elif targetstr == 'target_label':
                    targetstr = 'int ' + targetstr
                elif targetstr == 'max_val' and isinstance(chlist[1], ast.Num):
                    targetstr = 'float ' + targetstr
                st = self.get_indent() + targetstr + ' = ' + valuestr + ';'

            return st
        elif isinstance(node, ast.AugAssign):
            chlist = ast_visitor.get_chlist(self, node)
            # print 'AugAssign: childs = ', len(chlist)
            targetstr, targetname = ast_visitor.getAssignTarget(self, chlist[0])
            operatorstr = ast_visitor.getOperator(self, chlist[1])
            valuestr, valuelist = ast_visitor.getAssignValue(self, chlist[2])
            st = self.get_indent() + targetstr + ' ' + operatorstr + '= ' + valuestr + ';'
            return st
        elif isinstance(node, ast.Expr):
            print '    Expr: '
            chlist = ast_visitor.get_chlist(self, node)
            st, valuelist = ast_visitor.getAssignValue(self, chlist[0])
            targetname = valuelist[0] + valuelist[1]
            if self.state == 0:
                TopfileSymbolTable[targetname] = valuelist
            return self.get_indent() + st + ';'
        elif isinstance(node, ast.For):
            st = ast_visitor.getFor(self, node)
            return st
        elif isinstance(node, ast.Return):
            chlist = ast_visitor.get_chlist(self, node)
            # print 'Return: childs = ', len(chlist)
            valuestr, valuelist = ast_visitor.getAssignValue(self, chlist[0])
            st = 'return '+ valuestr
            # for ch in ast.iter_child_nodes(node):
            #     print '        ', ch
            return self.get_indent() + st + ';'
        elif isinstance(node, ast.FunctionDef):
            if node.name == 'forward':
                # print '!This forward'
                forward_func_ast.append(node)
            elif node.name == 'backward':
                # print '!This backward'
                backward_func_ast.append(node)
            elif 'mapping' in node.name:
                # print '!This mapping'
                mapping_func_ast.append(node)         
            else:
                chlist = ast_visitor.get_chlist(self, node)
                print 'FunctionDef: Name = ', node.name
                actual = ast_visitor.getActuals(self, chlist[0])
                st += self.get_indent() + 'int ' + node.name + actual + ' {\n'
                self.indent += 4
                for ch in chlist[1:]:
                    #print chch
                    st += ast_visitor.getStatement(self, ch)
                    st += '\n'
                st += self.get_indent() + '}\n'
            return st
        elif isinstance(node, ast.Pass):
            return ''
                    # ast_visitor.self.get_indent(self, indent)
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


    def getActuals(self, node):
        stractuallist = []
        strdefaultlist = []
        actuallist = []
        # defaultlist = []
        st = '('
        print '    printing Actuals:'
        for ch in ast.iter_child_nodes(node):
            #print '!!!!!!!',ch
            if isinstance(ch, ast.Name):
                print '        ActName:', ch.id
                stractuallist.append(ch.id)
                actuallist.append(ch.id)
            elif isinstance(ch, ast.Num):
                print '        ActDefNum:', ch.n
                strdefaultlist.append(str(ch.n))
                actuallist.append(ch.n)
            elif isinstance(ch, ast.Str):
                print '        ActDefStr:', ch.s
                strdefaultlist.append(ch.s)
                actuallist.append(ch.s)
            else:
                print 'Unknown args'
        print
        for i in range(len(strdefaultlist)):
            stractuallist[-1-i] += ' = ' + strdefaultlist[i]
        for tmpst in stractuallist:
            st += tmpst + ', '
        if st[-1] == '(' :
            return '()', []
        else:
            return st[0:-2] + ')' , actuallist

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
        targetname = st
        return st, targetname

    def getAssignValue(self, node):
        #print '    AssignValue:', node
        st = ''
        valuelist = []
        if isinstance(node, ast.Num):
            print '        Num: ', node.n
            st = str(node.n)
            valuelist.append('Num')
            valuelist.append(str(node.n))
        elif isinstance(node, ast.Name):
            print '        Name: ', node.id
            st = node.id
            valuelist.append('Name')
            valuelist.append(node.id)
        elif isinstance(node, ast.Str):
            print '        Name: ', node.s
            st = node.s
            valuelist.append('Str')
            valuelist.append(node.s)
        elif isinstance(node, ast.Call):
            # for ch in ast.iter_child_nodes(node):
            #     print "            CallChildren: ", ch
            chlist = ast_visitor.get_chlist(self, node)
            callname = ast_visitor.getCallName(self, chlist[0])
            st +=  callname + '('
            valuelist.append('Call')
            valuelist.append(callname)
            callparam = []
            for ch in chlist[1:]:
                onecallparam = ast_visitor.getCallParams(self, ch)
                st +=  onecallparam + ', '
                callparam.append(onecallparam)
            valuelist.append(callparam)
            # print 'valuelist: ', valuelist
            if st[-1] == '(':
                return st + ')', valuelist
            else:
                return st[:-2] + ')' , valuelist
        elif isinstance(node, ast.Subscript):
            st = ast_visitor.getSubscript(self, node)
        elif isinstance(node, ast.Attribute):
            st = ast_visitor.getAttribute(self, node)
        elif isinstance(node, ast.BinOp):
            print '        BinOp: '
            chlist = ast_visitor.get_chlist(self, node)
            left, leftlist = ast_visitor.getAssignValue(self, chlist[0])
            operater = ast_visitor.getOperator(self, chlist[1])
            right, leftlist = ast_visitor.getAssignValue(self, chlist[2])
            st = left + ' ' + operater + ' ' + right
        elif isinstance(node, ast.Tuple):
            st, tuplelist= ast_visitor.getTuple(self, node)
            valuelist.append('Tuple')
            valuelist.append(tuplelist)
        elif isinstance(node, ast.List):
            st = ast_visitor.getList(self, node)
        else:
            st = 'Unknown Expr'
        return st, valuelist

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
        # print '    printing FuncParam:'
        if isinstance(node, ast.Name):
            # print '        ParamName:', node.id
            st = node.id
        elif isinstance(node, ast.Num):
            # print '        ParamNum:', node.n
            st = str(node.n)
        elif isinstance(node, ast.Str):
            # print '        ParamStr:', node.s
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

        st = self.get_indent()
        st += 'for ({} = {} ; {} < {} ; {} ++)'.format( ob, start, ob, end , ob)
        st += ' { \n'
        self.indent += 4
        for ch in chlist[2:]:
            st += ast_visitor.getStatement(self, ch) + '\n'
        self.indent -= 4
        st += self.get_indent() + '}'
        return st
    

    def getOperator(self, node):
        if isinstance(node, ast.Add):
            # print '        + '
            return '+'
        elif isinstance(node, ast.Sub):
            # print '        - '
            return '-'
        elif isinstance(node, ast.Mult):
            # print '        * '
            return '*'
        elif isinstance(node, ast.Div):
            # print '        / '
            return '/'
        else:
            print 'Unknown operater'

    def getTuple(self, node):
        strtuplelist = []
        tuplelist = []
        print '        TargetTuple('
        for ch in ast.iter_child_nodes(node):
            if isinstance(ch, ast.Name):
                print '            TupleName:', ch.id
                strtuplelist.append(ch.id)
                tuplelist.append(ch.id)
            elif isinstance(ch, ast.Num):
                print '            TupleNum:', ch.n
                strtuplelist.append(ch.n)
                tuplelist.append(str(ch.n))
            elif isinstance(ch, ast.Load):
                print '            TupleLoad'
            elif isinstance(ch, ast.Store):
                print '            TupleStore'
            else:
                print 'unknown type in getTuple'
        print '                )'
        st = str(strtuplelist)
        st = '{' + st[1:-1] + '}'
        return st, tuplelist

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

    def getFunctionDef(self, node):
        if isinstance(node, ast.FunctionDef):
            # print node.name
            return node.name




class ast_transformer(ast.NodeTransformer):
    def __init__(self):
        self.old_name = []
        self.new_name = []
        self.inputlength = 0
        self.length = 0
        self.if_add_dim = False

    def setParam(self, old_name, new_name, inputlength, length, if_add_dim):
        self.old_name = old_name
        self.new_name = new_name
        self.inputlength = inputlength
        self.length = length
        self.if_add_dim = if_add_dim

    def visit_FunctionDef(self, node):
        self.generic_visit(node)
        if self.if_add_dim:
            node.body = [ast.For(target=ast.Name(id='j', ctx=ast.Store()),
                                 iter=ast.Call(func = ast.Name(id = 'range', ctx = ast.Load()),
                                               args = [ast.Num(n=0), ast.Num(n=self.length)],
                                               keywords=[],
                                               starargs= None,
                                               kwargs=None
                                               ),
                                 body = node.body,
                                 orelse=[]
                )]
            return node
        else:
            return node

    def visit_Call(self, node):
        self.generic_visit(node)
        if node.func.id == 'len':
            return ast.copy_location(ast.Num(n = self.inputlength), node)
        return node

    def visit_Subscript(self, node):
        if self.if_add_dim:
            if isinstance(node.value, ast.Attribute):
                index = self.find_str(node.value.value.id)
                if index != -1:
                    node.value = ast.Name(id = self.new_name[index] + '_' + node.value.attr , ctx = node.ctx)
                # node.value = ast.Subscript(value = node.value ,
                #                            slice = ast.Index(value=Name(id='j', ctx =Load())),
                #                            ctx = node.ctx
                #                            )
                # if not isinstance(node.value, ast.Name):
                #     node.slice = ast.Index(value=Name(id='j*'+str(self.length)+' + i'))
                # else:
                #     if 'gd_input' in node.value.id:
                #         node.slice = node.slice
                #     else:
                #         node.slice = ast.Index(value=Name(id='j*'+str(self.length)+' + i'))
                if isinstance(node.value, ast.Name):
                    index = self.find_shared_buffer(node.value.id)
                    if index == -1:
                        node.slice = ast.Index(value=Name(id='j*'+str(self.inputlength)+' + i'))
                    else:
                        node.value.id = shared_buffer_list[index]
                elif isinstance(node.value, ast.Attribute):
                    node.slice = ast.Index(value=Name(id='j*'+str(self.inputlength)+' + i'))
            elif isinstance(node.value, ast.Name):
                index = self.find_str(node.value.id)
                if index != -1:
                    node.value.id = self.new_name[index]
                # node.value = ast.Subscript(value = node.value ,
                #                            slice = ast.Index(value=Name(id='j', ctx =Load())),
                #                            ctx = node.ctx
                #                            )
                node.slice = ast.Index(value=Name(id='j*'+str(self.inputlength)+' + i'))
        else:
            if isinstance(node.value, ast.Attribute):
                index = self.find_str(node.value.value.id)
                if index != -1:
                    node.value = ast.Name(id = self.new_name[index] + '_' + node.value.attr , ctx = node.ctx)
            elif isinstance(node.value, ast.Name):
                index = self.find_str(node.value.id)
                if index != -1:
                    node.value.id = self.new_name[index]
        return node

    def visit_Attribute(self, node):
        #self.generic_visit(node)
        # for ch in ast.iter_fields(node):
        #     print '        Fields', ch
        # print
        if self.if_add_dim:
            index = self.find_str(node.value.id)
            if index != -1:
                node = ast.Subscript(value = ast.Name(id = self.new_name[index] + '_' + node.attr , ctx = node.ctx),
                                     slice = ast.Index(value=Name(id='j', ctx =Load())),
                                     ctx = node.ctx
                                    )
            else:
                node = ast.Subscript(value = node,
                                     slice = ast.Index(value=Name(id='j', ctx =Load())),
                                     ctx = node.ctx
                                    )
        return node

    def get_chlist(self, node):
        chlist = []
        for ch in ast.iter_child_nodes(node):
            chlist.append(ch)
        return chlist 

    def find_str(self, str):
        length = len(self.old_name)
        index = -1
        for i in range(length):
            if str == self.old_name[i]:
                index = i
        return index

    def find_shared_buffer(self, str):
        length = len(shared_buffer_list)
        index = -1
        for i in range(length):
            if str in shared_buffer_list[i]:
                index = i
        return index


def initStructure():
    for key in TopfileSymbolTable.keys():
        value = TopfileSymbolTable[key]
        if value[0] == 'Call' and value[1] == 'Net':
            net.name = key
            net.batch_size = searchNum(value[2][0])
            break

    for key in LayerNameList:
        value = TopfileSymbolTable[key]
        net.ensemble_list.append(EnsembleNode(value[1], key))

    counter = 0
    for key in LayerNameList:
        value = TopfileSymbolTable[key]
        if value[1] == 'MemoryDataLayer':
            net.ensemble_list[counter].ensemble_type += 'DataEnsemble'
            net.ensemble_list[counter].neuron_type += 'DataNeuron'
        elif value[1] == 'SoftmaxLossLayer':
            net.ensemble_list[counter].ensemble_type += 'NormalizationEnsemble'
            net.ensemble_list[counter].neuron_type += 'SoftmaxLossNeuron'
        else:
            net.ensemble_list[counter].ensemble_type += 'Ensemble'
            net.ensemble_list[counter].neuron_type += 'WeightedNeuron'
        counter += 1

    counter = 0
    for ens in net.ensemble_list:
        if counter == 0:
            ens.ensemble_fields_list.append(FieldsNode('name', 'Str', 'data'))
            ens.ensemble_fields_list.append(FieldsNode('neurons', 'Array', 'zeros'))
            ens.ensemble_fields_list.append(FieldsNode('value', 'Array', 'load'))
            ens.ensemble_fields_list.append(FieldsNode('connection', 'List', 'Empty'))
            ens.ensemble_fields_list.append(FieldsNode('phase', 'Str', 'TrainTest'))
            ens.ensemble_fields_list.append(FieldsNode('net_subgroup', 'Num', '1'))
            ens.neuron_size = eval(TopfileSymbolTable['shape'][1][0])
            ens.neuron_fields_list.append(FieldsNode('value', 'Num', '0'))
            ens.neuron_fields_list.append(FieldsNode('gd_value', 'Num', '0'))
        elif counter == 1:
            ens.ensemble_fields_list.append(FieldsNode('name', 'Str', 'label'))
            ens.ensemble_fields_list.append(FieldsNode('neurons', 'Array', 'zeros'))
            ens.ensemble_fields_list.append(FieldsNode('value', 'Array', 'load'))
            ens.ensemble_fields_list.append(FieldsNode('connection', 'List', 'Empty'))
            ens.ensemble_fields_list.append(FieldsNode('phase', 'Str', 'TrainTest'))
            ens.ensemble_fields_list.append(FieldsNode('net_subgroup', 'Num', '1'))
            ens.neuron_size = eval(TopfileSymbolTable['shapelabel'][1][0])
            ens.neuron_fields_list.append(FieldsNode('value', 'Num', '0'))
            ens.neuron_fields_list.append(FieldsNode('gd_value', 'Num', '0'))
        elif counter == 2:
            ens.ensemble_fields_list.append(FieldsNode('net', 'Var', 'net'))
            ens.ensemble_fields_list.append(FieldsNode('name', 'Str', 'fc1'))
            ens.ensemble_fields_list.append(FieldsNode('neurons', 'Assign'))
            ens.ensemble_fields_list.append(FieldsNode('params', 'Assign'))
            ens.ensemble_fields_list.append(FieldsNode('batch_size', 'Num', '1'))
            ens.neuron_size = 100
            ens.neuron_fields_list.append(FieldsNode('value', 'Num', '0'))
            ens.neuron_fields_list.append(FieldsNode('gd_value', 'Num', '0'))
            ens.neuron_fields_list.append(FieldsNode('inputs', 'Array', '0', 250))
            ens.neuron_fields_list.append(FieldsNode('gd_inputs', 'Array', '0', 250))
            ens.neuron_fields_list.append(FieldsNode('weights', 'Array', 'xavier', 250))
            ens.neuron_fields_list.append(FieldsNode('gd_weights', 'Array', 'zeros', 250))
            ens.neuron_fields_list.append(FieldsNode('bias', 'Array', 'zeros'))
            ens.neuron_fields_list.append(FieldsNode('gd_bias', 'Array', 'zeros'))
            ens.params.append(ParamNode('fc1', 'weights', 1.0 , 1.0))
            ens.params.append(ParamNode('fc1', 'bias', 2.0 , 0.0))
            ens.source_list.append(SourceNode(net.ensemble_list[0], [0, eval(TopfileSymbolTable['shape'][1][0]) - 1], False, 250))
        elif counter == 3 :
            ens.ensemble_fields_list.append(FieldsNode('net', 'Var', 'net'))
            ens.ensemble_fields_list.append(FieldsNode('name', 'Str', 'fc2'))
            ens.ensemble_fields_list.append(FieldsNode('neurons', 'Assign'))
            ens.ensemble_fields_list.append(FieldsNode('params', 'Assign'))
            ens.ensemble_fields_list.append(FieldsNode('batch_size', 'Num', '1'))
            ens.neuron_size = 10
            ens.neuron_fields_list.append(FieldsNode('value', 'Num', '0'))
            ens.neuron_fields_list.append(FieldsNode('gd_value', 'Num', '0'))
            ens.neuron_fields_list.append(FieldsNode('inputs', 'Array', '0', 100))
            ens.neuron_fields_list.append(FieldsNode('gd_inputs', 'Array', '0', 100))
            ens.neuron_fields_list.append(FieldsNode('weights', 'Array', 'xavier', 100))
            ens.neuron_fields_list.append(FieldsNode('gd_weights', 'Array', 'zeros', 100))
            ens.neuron_fields_list.append(FieldsNode('bias', 'Array', 'zeros'))
            ens.neuron_fields_list.append(FieldsNode('gd_bias', 'Array', 'zeros'))
            ens.params.append(ParamNode('fc2', 'weights', 1.0 , 1.0))
            ens.params.append(ParamNode('fc2', 'bias', 2.0 , 0.0))
            ens.source_list.append(SourceNode(net.ensemble_list[2], [0, 99], False, 100))
        elif counter == 4 :
            ens.ensemble_fields_list.append(FieldsNode('name', 'Str', 'loss'))
            ens.ensemble_fields_list.append(FieldsNode('neurons', 'Array', 'zeros'))
            ens.ensemble_fields_list.append(FieldsNode('connection', 'Empty'))
            ens.ensemble_fields_list.append(FieldsNode('num_inputs', 'Num', '10'))
            ens.ensemble_fields_list.append(FieldsNode('phase', 'Str', 'Train'))
            ens.neuron_size = 1
            ens.neuron_fields_list.append(FieldsNode('prob', 'Num', '0'))
            ens.neuron_fields_list.append(FieldsNode('gd_value', 'Num', '0'))
            ens.source_list.append(SourceNode(net.ensemble_list[3], [0, 9], False, 10))
            ens.source_list.append(SourceNode(net.ensemble_list[1], [0, 0], False, 1))
        counter += 1

class Task:
    def __init__(self, func, arg_list):
        self.func = func
        self.arg_list = arg_list

class NetNode:
    def __init__(self):
        self.name = ''
        self.ensemble_list = []
        self.buffer_list = OrderedDict()
        self.batch_size = 1
        self.forward_task_list = []
        self.backward_task_list = []
        self.batch_size = batch_size
        # self.foward_body = {"Train":[], "Test":[]}
        # self.foward_args = {"Train":Set(), "Test":Set()}
        # self.backward_body = {"Train":[], "Test":[]}
        # self.backward_args = {"Train":Set(), "Test":Set()} 
        
    def printNetNode(self):
        print 'NetName = ', self.name
        print 'BatchSize = ', self.batch_size
        print 'ensemble_list = '
        for ens in self.ensemble_list:
            print ' ', ens.ensemble_type, ' ', ens.neuron_type, ' ', ens.neuron_size

class EnsembleNode:
    def __init__(self, name, name2):
        self.ensemble_name = name
        self.ensemble_type = ''
        self.ensemble_fields_list = []
        #self.ensemble_actuals_list = []
        self.neuron_size = 0
        self.neuron_type = ""
        self.neuron_fields_list = []
        self.source_list = []
        self.forward_ast = None #body ast
        self.backward_ast = None #body ast
        self.forward_actuals_list = []
        self.backward_actuals_list = []
        self.params = []
        self.name = name2

class ParamNode:
    def __init__(self, en_name, attr, learning_rate, regu_coef):
        self.name = en_name + "_" + attr
        self.gradient_name = en_name + "_gd_" + attr
        self.hist_name = en_name + "_" + attr + "_hist"
        self.learning_rate = learning_rate
        self.regu_coef = regu_coef
        self.value = None
        self.gd_value = None
        self.hist = None


class FieldsNode:
    def __init__(self, name, typein, init = '', size = 1):
        self.name = name
        self.type = typein
        self.init = init
        self.size = size

class ActualNode:
    def __init__(self):
        self.name = ""
        self.type = ""
        #self.value

class SourceNode:
    def __init__(self, ens, mapping, copy, size):
        self.source_ensemble = ens
        self.mapping_ast = None
        self.is_dim_fixed = True
        self.is_one_to_one = False
        self.copy = copy
        self.size = size
        self.shape = None


def searchNum(string):
    value = TopfileSymbolTable[string]
    if value[0] == 'Num':
        return eval(value[1])
    else:
        return -1

def transform_fn(ensemble):
    pass

def remove_line_nodes(ast):
    pass

def drop_fixed_dims(ast, arg_info):
    pass

def add_neuron_loop(body, args, value):
    pass

def gen_copy_block(ensemble, net, index):
    return ""

def gen_forward(ensemble, net):
    body = []
    args = []
    buff = net.buffer_list[ensemble.name + "_value"]
    for(index, src) in enumerate(ensemble.source_list):
        sink = ensemble.name + "_inputs_" + str(index)
        ensemble.arg_info[sink] = src.is_dim_fixed
        if src.copy:
            args.append(src.source_ensemble.name + "_value")
            ast = gen_copy_block(ensemble, net, index)
            body.append(ast)

    transform_fn(ensemble)


def norm_forward(ensemble, net):
    pass

num_of_threads = 4;

class Buffer:
    def __init__(self, new = True, src = None, reshape = False):
        self.init_func = None
        self.shape = None
        self.name = None 
        self.new = new
        self.src = src
        self.reshape = reshape
        self.clear = True


def main():
    global net, output_file

    initLayerDict()
    net = NetNode()

    topfile = sys.argv[1]
    print('=' * 50)
    print('Latte Compiler: Processing ', topfile)
    print('=' * 50)
    ftop = open(topfile)
    top_expr = ftop.read()
    ftop.close()
    top_ast = ast.parse(top_expr)
    #ast_print(topfile, top_ast) 

    x = ast_visitor()
    x.visit(top_ast)

    #print TopfileSymbolTable
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(TopfileSymbolTable)
    print

    initStructure()
    net.printNetNode()

    n_epoch = eval(TopfileSymbolTable['n_epoch'][1])
    update_rate = eval(TopfileSymbolTable['update_rate'][1])
    for keys in TopfileSymbolTable.keys():
        if ('data' in keys ) and ('file' in keys ):
            load_data_path.append(TopfileSymbolTable[keys][1])
    for keys in TopfileSymbolTable.keys():
        if ('label' in keys ) and ('file' in keys ):
            load_data_path.append(TopfileSymbolTable[keys][1])

    x.state = 1 #Finding Forward and Backward
    for ens in net.ensemble_list:
        ens_type = ens.ensemble_name
        filepath = LayerDict[ens_type]
        f = open(filepath)
        fcontent = f.read()
        layer_ast = ast.parse(fcontent)
        x.visit(layer_ast)
        f.close()
    x.state = 2

    counter = 0
    for ens in net.ensemble_list:
        ens.forward_ast = forward_func_ast[counter]
        ens.backward_ast = backward_func_ast[counter]
        ens.forward_actuals_list = forward_func_actuals[counter]
        ens.backward_actuals_list = backward_func_actuals[counter]
        counter += 1


    for ensemble in net.ensemble_list:
        for field in ensemble.neuron_fields_list:
            if ensemble.ensemble_type == "NormalizationEnsemble":
                buff2 = Buffer()
                buff2.init_func = "zeros"
                buff2.shape = (1,1)
                buff2.name = ensemble.name + "_value"
                net.buffer_list[buff2.name] = buff2
            elif field.name == "inputs" or field.name == "gd_inputs":
                pass
            elif field.name == "value" or field.name == "gd_value":
                buff = Buffer()
                buff.init_func = "zeros"
                buff.shape = (ensemble.neuron_size, net.batch_size)
                buff.name = ensemble.name + "_" + field.name
                net.buffer_list[buff.name] = buff
            elif field.type != "Num":
                buff = Buffer()
                buff.init_func = field.init
                buff.shape = (field.size, ensemble.neuron_size)
                buff.name = ensemble.name + "_" + field.name
                if field.name == "weights" or field.name == "bias":
                    buff.clear = False
                net.buffer_list[buff.name] = buff
            else:
                buff = Buffer()
                buff.init_func = field.init
                buff.shape = (ensemble.neuron_size,1)
                buff.name = ensemble.name + "_" + field.name
                net.buffer_list[buff.name] = buff

    for ensemble in net.ensemble_list:
        for field in ensemble.neuron_fields_list:
            if field.name == "inputs" or field.name == "gd_inputs" or field.name == "prob":
                attr = ""
                if field.name == "inputs":
                    attr = "value"
                elif field.name == "gd_inputs":
                    attr = "gd_value"
                else:
                    attr = "gd_value"
                for (index, src) in enumerate(ensemble.source_list):
                    key = ensemble.name + "_" + field.name + "_" + str(index)
                    src_buff = src.source_ensemble.name + "_" + attr
                    if src_buff in net.buffer_list:
                        if src.is_dim_fixed: #all
                            src.copy = False
                            buff = Buffer(False, net.buffer_list[src_buff], True)
                            buff.shape = (src.size, net.batch_size)
                            buff.name = key
                            net.buffer_list[buff.name] = buff
                            shared_buffer_list.append(key)
                        elif src.is_one_to_one:
                            src.copy = False
                            buff = Buffer(False, net.buffer_list[src_buff])
                            buff.name = key
                            net.buffer_list[buff.name] = buff
                            shared_buffer_list.append(key)
                        else:
                            src.copy = True
                            buff = Buffer()
                            buff.shape = (src.size, ensemble.neuron_size)
                            buff.name = key
                            net.buffer_list[buff.name]
                    else:
                        buff = Buffer()
                        buff.init_func = field.init
                        #TODO
                        buff.shape = (1,1)
                        buff.name = key
                        net.buffer_list[buff.name] = buff

    for ensemble in net.ensemble_list:
        if ensemble.ensemble_type == "DataEnsemble":
            name = ensemble.name + '_' + ensemble.forward_actuals_list[0]
            load_buffer_list.append(name)
            load_buffer_list_size.append(ensemble.neuron_size)
        if ensemble.ensemble_type == "NormalizationEnsemble":
            name1 = ensemble.name + "_value"
            output_buffer.append(name1)
            output_buffer_size.append(net.buffer_list[name1].shape[0] * net.buffer_list[name1].shape[1])
            name2 = ensemble.name + "_prob_0"
            output_buffer.append(name2)
            output_buffer_size.append(net.buffer_list[name2].shape[0] * net.buffer_list[name2].shape[1])



    for key, value in net.buffer_list.iteritems():
        print key, value.shape


    # for ensemble in net.ensemble_list:
    #     if ensemble.ensemble_type == "DataEnsemble":
    #         net.forward_task_list.append(Task("forward", ensemble.forward_actuals_list))
    #     elif ensemble.ensemble_type == "Ensemble":
    #         gen_forward(ensemble, net)
    #     else: #normalization
    #         norm_forward(ensemble, net)



#========================================================================================================

    output_file = open('dnn.cpp', 'w+a')
    output_file.write("#include \"solver.h\"\n")
    output_file.write("int i = 0, j = 0;\n")
    for i in range(len(load_buffer_list)):
        output_file.write('float* '+load_buffer_list[i]+' = new float['+str(load_buffer_list_size[i])+'];\n')


    for key, value in net.buffer_list.iteritems():
        if value.new:
            output_file.write("float* " + key + " = " + value.init_func + "(" + str(value.shape[0]) + ", " + str(value.shape[1]) + ", 1);\n")
            allocated_buffer_list.append(key)
        else:
            output_file.write("float* " + key + " = " + value.src.name + ";\n")


    y = ast_transformer()

    y.setParam(['value', 'loaddata'], ['data_value', load_buffer_list[0]], 250, 250, False)
    y.visit(forward_func_ast[0])
    y.setParam(['value', 'loaddata'], ['label_value', load_buffer_list[1]], 1, 1, False)
    y.visit(forward_func_ast[1])
    y.setParam(['neuron'], ['fc1'], 250, 100, True)
    y.visit(forward_func_ast[2])
    y.setParam(['neuron'], ['fc2'], 100, 10, True)
    y.visit(forward_func_ast[3])
    y.setParam(['loss', 'prob', 'input', 'label'], ['loss_value', 'loss_prob_0', 'fc2_value', 'label_value'], 10, 10, False)
    y.visit(forward_func_ast[4])
    y.setParam(['loss', 'prob', 'input', 'label'], ['loss_value', 'loss_prob_0', 'fc2_value', 'label_value'], 10, 10, False)
    y.visit(backward_func_ast[4])
    y.setParam(['neuron'], ['fc2'], 100, 10, True)
    y.visit(backward_func_ast[3])
    y.setParam(['neuron'], ['fc1'], 250, 100, True)
    y.visit(backward_func_ast[2])
    y.setParam(['value', 'loaddata'], ['label_value', load_buffer_list[1]], 1, 1, False)
    y.visit(backward_func_ast[1])
    y.setParam(['value', 'loaddata'], ['data_value', load_buffer_list[0]], 1, 250, False)
    y.visit(backward_func_ast[0])

    
    output_file.write("\n\nvoid forward() {\n")
    for i in range(len(forward_func_ast)):
        x.visit(forward_func_ast[i])
    output_file.write("}")

    output_file.write("\n\nvoid backward() {\n")
    for i in range(len(backward_func_ast)):
        x.visit(backward_func_ast[len(backward_func_ast) - 1 - i])
    output_file.write("}")

    output_file.write("\n\nvoid update() {\n")
    for ensemble in net.ensemble_list:
        if ensemble.ensemble_type == "Ensemble":
            for param in ensemble.params:
                d1 = net.buffer_list[param.name].shape[0]
                d2 = net.buffer_list[param.name].shape[1]
                output_file.write("    for(i = 0; i < " + str(d2) + "; ++i){\n")
                output_file.write("        for(j = 0; j < " + str(d1) + "; ++j){\n")
                output_file.write("            " + param.name + "[i * " + str(d1)+ " + j] -= " + str(update_rate) + '*' + param.gradient_name + "[i * " + str(d1)+ " + j];\n")
                output_file.write("        }\n")
                output_file.write("    }\n")
    output_file.write("}")


    output_file.write("\n\n\nint main(){\n")

    for i in range(len(load_buffer_list)):
        output_file.write('    string s' + str(i) + ' = ' + '\"' + load_data_path[i] + '\";\n') 

    for i in range(len(load_buffer_list)):
        output_file.write('    load_data('+load_buffer_list[i]+', '
                               +str(load_buffer_list_size[i]) +', '
                               + 's' + str(i) + ');\n'
                               )

    output_file.write('\n')
    output_file.write("    vector<float*> buff;\n")
    output_file.write("    vector<int> dim;\n\n")
    for key, value in net.buffer_list.iteritems():
        if value.new:
            if value.clear:
                output_file.write("    buff.push_back(" + key + ");\n")
                output_file.write("    dim.push_back(" + str(value.shape[0]*value.shape[1]) + ");\n")
            else:
                print key + "     NOT CLEAR"

    output_file.write('\n')
    output_file.write("    for ( int k = 0 ; k < " + str(n_epoch) + " ; k ++ ) {\n")
    output_file.write("        forward();\n")
    output_file.write("        printf(\"" + output_buffer[0] + " = %f\\n\", " + output_buffer[0] + "[0]);\n")
    output_file.write("        backward();\n")
    output_file.write("        update();\n")
    output_file.write("        clear_buffer(buff, dim);\n")
    output_file.write("    }\n\n")


    for string in allocated_buffer_list:
        output_file.write('    delete []' + string + ';\n')
    for string in load_buffer_list:
        output_file.write('    delete []' + string + ';\n')


    output_file.write("    return 0;\n")
    output_file.write("}")

    # print "SHARED\n"
    # for key in shared_buffer_list:
    #     print key

    # print n_epoch
    print load_data_path
    print load_buffer_list
    print output_buffer
    print update_rate


'''
    x.state = 2
    #for i 

    for i in ast.iter_fields(ch):
        print i
'''

if __name__ == "__main__":
    main()
    

    

