#!/usr/bin/env python3

# requirements: phply

from phply import phplex
from phply.phpparse import make_parser
from phply.phpast import *
from pprint import pprint as pp

class Method(object):

    def __init__(self, name):
        self.name = name
        self.parameters = list()

    def add_parameter(self, parameter):
        self.parameters.append(parameter)

    def __str__(self):
        parameters_string = ", ".join([parameter_str.__str__() for parameter_str in self.parameters])
        return "%s ( %s )" % (self.name, parameters_string)

    def __repr__(self):
        return self.__str__()

    def __gt__(self, other):
        return self.name > other.name

class Parameter(object):

    def __init__(self, name):
        self.name = str(name)

    def __str__(self):
        return self.name

def collect_method(method_name, nodes, methods):
    for statement in nodes:
        if statement.__class__.__name__ == 'MethodCall':
            if (statement.name == method_name):
                method = Method(statement.params[0].node)
                for idx in range(1, len(statement.params)):
                    param = statement.params[idx]
                    if hasattr(param, 'node') and param.node.__class__.__name__ == 'Array':
                        for elem in param.node.nodes:
                            method.add_parameter(Parameter(elem.key))
                methods.append(method)
        elif hasattr(statement, 'nodes'):
            collect_method(method_name, statement.nodes, methods)
        elif hasattr(statement, 'node'):
            collect_method(method_name, [statement.node], methods)

def main():
    """
    Parse PHP files, finding occurrences of SOAP calls. Record operation name and parameters.
    Useful for documentation.
    """

    methods = list()

    parser = make_parser()
    lexer = phplex.lexer.clone()

    with open('input.php') as f:
        output = parser.parse(f.read(), lexer=lexer)

        # namespace is 0 normally... and will assume we have just a single class in the file...
        class_decl = output[1]

        for class_node in class_decl.nodes:
            if class_node.__class__.__name__ == 'Method':
                collect_method('doServiceGET', class_node.nodes, methods)

    methods.sort()
    for method in methods:
        pp(method)

if __name__ == '__main__':
    main()
