#!/usr/bin/env python
# code extracted from: http://rosettacode.org/wiki/S-Expressions

from __future__ import print_function
import re

dbg = False
float_render = "%.2f"

term_regex = r'''(?mx)
    \s*(?:
        (?P<brackl>\()|
        (?P<brackr>\))|
        (?P<num>[+-]?\d+\.\d+(?=[\ \)])|\-?\d+(?=[\ \)]))|
        (?P<sq>"[^"]*")|
        (?P<s>[^(^)\s]+)
       )'''

def parse_sexp(sexp):
    stack = []
    out = []
    if dbg: print("%-6s %-14s %-44s %-s" % tuple("term value out stack".split()))
    for termtypes in re.finditer(term_regex, sexp):
        term, value = [(t,v) for t,v in termtypes.groupdict().items() if v][0]
        if dbg: print("%-7s %-14s %-44r %-r" % (term, value, out, stack))
        if   term == 'brackl':
            stack.append(out)
            out = []
        elif term == 'brackr':
            assert stack, "Trouble with nesting of brackets"
            tmpout, out = out, stack.pop(-1)
            out.append(tmpout)
        elif term == 'num':
            v = float(value)
            if v.is_integer(): v = int(v)
            out.append(v)
        elif term == 'sq':
            out.append(value[1:-1])
        elif term == 's':
            out.append(value)
        else:
            raise NotImplementedError("Error: %r" % (term, value))
    assert not stack, "Trouble with nesting of brackets"
    return out[0]
    
class SexprBuilder(object):
    def __init__(self, key, *arg, **kwarg):
        
        self.key = key
        self.indent = kwargs.get('indent', 0)
    
        self.indent = kwargs.get('indent', 0)
        self.key = None
        self.output = ''
        self.items = []
        
    # Move to new line (optionally indent)
    def newline(self, indent=False):
        self.output += "\n"
        if indent:
            self.indent += 1
        self.output += 2 * self.indent * ' '
        
    def begin(self, key=None):
        self.key = key
        self.items = []
        
        self.output += '('
        if key:
            self.output += str(key)
        
    def add(self, item):
        self.items.append(item)
        
    def end(self, newline=False):
        self.output.append()
    
# Form a valid sexpr (single line)
def SexprItem(val, key=None):
    if key:
        fmt = "(" + key + " {val})"
    else:
        fmt = "{val}"
    
    t = type(val)
    
    if val is None or t == str and len(val) == 0:
        val = '""'
    elif t in [list, tuple]:
        val = ' '.join([SexprItem(v) for v in val])
    elif t == dict:
        values = []
        for key in val.keys():
            values.append(SexprItem(val[key],key))
        val = ' '.join(values)
    elif t == float:
        val = str(round(val,10)).rstrip('0').rstrip('.')
    elif t == int:
        val = str(val)
    #elif t == float:
    #    val = float_render % val
    elif t == str and re.search(r'[\s()\"]', val):
        val = '"%s"' % repr(val)[1:-1].replace('"', '\"') 
    
    return fmt.format(val=val)
    
class SexprBuilder(object):
    def __init__(self, key):
        self.indent = 0
        self.output = ''
        self.items = []
        if key is not None:
            self.startGroup(key, newline=False)
       
    def _indent(self):
        self.output += ' ' * 2 * self.indent
   
    def _newline(self):
        self.output += '\n'
        
    def _addItems(self):
        self.output += ' '.join(map(str,self.items))
        self.items = []
       
    def startGroup(self, key=None, newline=True, indent=False):
        self._addItems()
        if newline and indent:
            self.indent += 1
        if newline:
            self._newline()
            self._indent()
        self.output += '('
        if key:
            self.output += str(key) + ' '
            
    def endGroup(self, newline=True):
        self._addItems()
        if newline:
            self._newline()
            if self.indent > 0:
                self.indent -= 1
            self._indent()
        self.output += ')'
        
    def addOptItem(self, key, item, newline=True, indent=False):
        if item in [None, 0, False]:
            return
            
        self.addItems({key: item}, newline=newline, indent=indent)
            
    def addItem(self, item, newline=True, indent=False):
        self._addItems()
        if newline and indent:
            self.indent += 1
        if newline:
            self.newLine()
        self.items.append(SexprItem(item))
            
    # Add a (preformatted) item
    def addItems(self, *arg, newline=True, indent=False):
        self._addItems()
        if indent:
            self.indent += 1
        if newline:
            self.newLine()
        for a in arg:
            self.items.append(SexprItem(a))
            
    def newLine(self, indent=False):
        self._addItems()
        self._newline()
        if indent:
            self.indent += 1
        self._indent()
        
    def unIndent(self):
        if self.indent > 0:
            self.indent -= 1
        
def build_sexp(exp, key=None):
    out = ''
    
    # Special case for multi-values
    if type(exp) == type([]):
        out += '('+ ' '.join(build_sexp(x) for x in exp) + ')'
        return out
    elif type(exp) == type('') and re.search(r'[\s()]', exp):
        out += '"%s"' % repr(exp)[1:-1].replace('"', '\"')
    elif type(exp) in [int,float]:
        out += float_render % exp
    else:
        if exp == '':
            out += '""'
        else:
            out += '%s' % exp
    
    if key is not None:
        out = "({key} {val})".format(key=key, val=out)
        
    return out

def format_sexp(sexp, indentation_size=2, max_nesting=2):
    out = ''
    n = 0
    for termtypes in re.finditer(term_regex, sexp):
        indentation = ''
        term, value = [(t,v) for t,v in termtypes.groupdict().items() if v][0]
        if term == 'brackl':
            if out:
                if n <= max_nesting:
                    if out[-1] == ' ': out = out[:-1]
                    indentation = '\n' + (' ' * indentation_size * n)
                else:
                    if out[-1] == ')': out += ' '
            n += 1
        elif term == 'brackr':
            if out and out[-1] == ' ': out = out[:-1]
            n -= 1
        elif term == 'num':
            value += ' '
        elif term == 'sq':
            value += ' '
        elif term == 's':
            value += ' '
        else:
            raise NotImplementedError("Error: %r" % (term, value))

        out += indentation + value

    out += '\n'
    return out

if __name__ == '__main__':
    sexp = ''' ( ( data "quoted data" 123 4.5)
         (data (123 (4.5) "(more" "data)")))'''

    print('Input S-expression: %r' % (sexp, ))
    parsed = parse_sexp(sexp)
    print("\nParsed to Python:", parsed)

    print("\nThen back to: '%s'" % build_sexp(parsed))