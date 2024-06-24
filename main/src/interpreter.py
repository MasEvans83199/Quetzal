# interpreter.py
import math_utils
import string_utils
import file_utils
from lexer import Lexer
from parser import Parser
from ast import (
    FunctionDeclaration,
    ForLoopNode,
    WhileLoopNode,
    DoWhileNode,
    IfNode,
    BinaryOperatorNode,
    NumberNode,
    VariableDeclarationNode,
    AssignNode,
    FunctionCallNode,
    OutputNode,
    VariableAccessNode,
    StringLiteralNode
)

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
        self.environment = {}

    def interpret(self, ast):
        results = []
        for node in ast:
            result = self.visit(node)
            if result is not None:
                results.append(result)
        return '\n'.join(filter(None, results))

    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.no_visit_method)
        return visitor(node)

    def visit_IfNode(self, node):
        condition_value = self.visit(node.condition)
        if condition_value:
            return self.visit_list(node.then_block)
        return None

    def visit_BinaryOperatorNode(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        return eval(f"{left} {node.operator} {right}")

    def visit_NumberNode(self, node):
        return node.value

    def visit_StringLiteralNode(self, node):
        return node.value

    def visit_CharacterNode(self, node):
        return node.value

    def visit_VariableDeclarationNode(self, node):
        self.environment[node.name] = self.visit(node.expression)
        return f"Variable '{node.name}' set to {self.environment[node.name]}"

    def visit_OutputNode(self, node):
        output_value = self.visit(node.value)
        return str(output_value)

    def visit_AssignNode(self, node):
        self.environment[node.name] = self.visit(node.expression)
        return f"Variable {node.name} assigned value {self.environment[node.name]}"

    def visit_VariableAccessNode(self, node):
        value = self.environment.get(node.identifier, "Undefined variable")
        return f"{node.identifier} = {value}"

    def visit_FunctionCallNode(self, node):
        func = global_namespace.get(node.function_name)
        if func:
            args = [self.visit(arg) for arg in node.arguments]
            return func(*args)
        raise NameError(f"Function {node.function_name} not defined")

    def visit_list(self, node_list):
        results = [self.visit(node) for node in node_list if node]
        return ' '.join(results)

    def no_visit_method(self, node):
        raise Exception(f'No visit_{type(node).__name__} method')

def run(code):
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    interpreter = Interpreter(parser)
    return interpreter.interpret(ast)

if __name__ == '__main__':
    code = 'string str : "Hello world"\n-> str'
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    interpreter = Interpreter(parser)
    result = interpreter.interpret(ast)
    print(result)
