import math
import numpy as np
from ast import *
import sys

def gaussian(mean=0.0, std=1.0, *args):
    gaussian_array = np.random.random(args)
    gaussian_array = gaussian_array*std - mean
    return gaussian_array

def xavier(*args):
    prod = 1;
    for i in range(0, len(args)-1) :
        prod *= args[i];
    scale = math.sqrt(3.0/prod)
    xavier_array = np.random.random(args)
    xavier_array = 2*scale*xavier_array - scale
    return xavier_array

def batch_size(net):
    return net.batch_size

class Param:
    def __init__(self, ensemble_name, name, learning_rate, regu_coef):
        self.name = ensemble_name + name
        self.gradient_name = ensemble_name + "_gd_" + name
        self.hist_name = ensemble_name + "_hist_" + name
        self.learning_rate = learning_rate
        self.regu_coef = regu_coef
        self.clip_gradients = -1.0
        self.value = []
        self.gradiend = []
        self.hist = []
        self.request = 0

def dump(node, annotate_fields=True, include_attributes=False, indent='  '):
    def _format(node, level=0):
        if isinstance(node, AST):
            fields = [(a, _format(b, level)) for a, b in iter_fields(node)]
            if include_attributes and node._attributes:
                fields.extend([(a, _format(getattr(node, a), level))
                               for a in node._attributes])
            return ''.join([
                node.__class__.__name__,
                '(',
                ', '.join(('%s=%s' % field for field in fields)
                           if annotate_fields else
                           (b for a, b in fields)),
                ')'])
        elif isinstance(node, list):
            lines = ['[']
            lines.extend((indent * (level + 2) + _format(x, level + 2) + ','
                         for x in node))
            if len(lines) > 1:
                lines.append(indent * (level + 1) + ']')
            else:
                lines[-1] += ']'
            return '\n'.join(lines)
        return repr(node)

    if not isinstance(node, AST):
        raise TypeError('expected AST, got %r' % node.__class__.__name__)
    return _format(node)

def parseprint(code, filename="<string>", mode="exec", **kwargs):
    """Parse some code from a string and pretty-print it."""
    node = parse(code, mode=mode)   # An ode to the code
    print(dump(node, **kwargs))

def ast_print(filename, expr):
    parseprint(expr, filename, include_attributes=False)
    print()


    
