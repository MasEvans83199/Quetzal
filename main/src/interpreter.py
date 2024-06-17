# interpreter.py
import math_utils
import string_utils
import file_utils
from lexer import Lexer
from parser import Parser

global_namespace = {
    'factorial': math_utils.factorial,
    'pow': math_utils.pow,
    'sqrt': math_utils.sqrt,
    'upper': string_utils.upper,
    'lower': string_utils.lower,
    'split': string_utils.split,
    'read_file': file_utils.read_file,
    'write_file': file_utils.write_file,
}

class Interpreter:
    def __init__(self, parser):
        self.parser = parser
        self.environment = global_namespace.copy()  # Start with a copy of the global namespace

    def interpret(self):
        # Interpret the parsed nodes
        result = None
        try:
            while True:
                node = self.parser.parse()
                if node is None:
                    break
                result = self.visit(node)
        except Exception as e:
            result = str(e)
        return result

    def visit(self, node):
        # Visitor method that calls the appropriate method based on node type
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.no_visit_method)
        return visitor(node)

    def no_visit_method(self, node):
        raise Exception(f'No visit_{type(node).__name__} method')

    # Add methods for visiting different types of nodes...
    # (Implementation of these methods based on the AST structure)

def run(code):
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    interpreter = Interpreter(parser)
    return interpreter.interpret()

# Example usage, this line can be commented out or removed.
# print(run('dec x : integer = 5; output -> x;'))
