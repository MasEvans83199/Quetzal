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
    ArrayDeclarationNode,
    ArrayAccessNode,
    FunctionCallNode,
    OutputNode,
    VariableAccessNode,
    IncrementNode,
    StopNode
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
        return '\n'.join(map(str, filter(None, results)))  # Ensure all results are strings

    def visit(self, node):
        print(f"Visiting: {type(node).__name__}")
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.no_visit_method)
        return visitor(node)

    def visit_ForLoopNode(self, node):
        start_value = self.environment[node.identifier]
        end_value = self.visit(node.end_value)
        results = []
        for i in range(start_value, end_value):
            self.environment[node.identifier] = i
            for stmt in node.body:
                result = self.visit(stmt)
                if result is not None:
                    results.append(result)
        return '\n'.join(map(str, results))  # Ensure all results are strings
    
    def visit_WhileLoopNode(self, node):
        results = []
        while self.visit(node.condition):
            print(f"Condition {node.condition} evaluated to True")  # Debug print
            for stmt in node.body:
                result = self.visit(stmt)
                if result is not None:
                    results.append(result)
            print(f"End of WHILE loop iteration, environment: {self.environment}")  # Debug print
        print(f"WHILE loop condition {node.condition} evaluated to False")  # Debug print
        return '\n'.join(map(str, results))  # Ensure all results are strings
    
    def visit_DoWhileNode(self, node):
        results = []
        while True:
            for stmt in node.body:
                result = self.visit(stmt)
                if result is not None:
                    results.append(result)
            if not self.visit(node.condition):
                break
            print(f"End of DO-WHILE loop iteration, environment: {self.environment}")  # Debug print
        print(f"DO-WHILE loop condition {node.condition} evaluated to False")  # Debug print
        return '\n'.join(map(str, results))  # Ensure all results are strings

    def visit_IncrementNode(self, node):
        if isinstance(node.identifier, ArrayAccessNode):
            array = self.environment[node.identifier.name]
            index = self.visit(node.identifier.index)
            array[index] += 1
            print(f"Incremented {node.identifier.name}[{index}], new value: {array[index]}")
        else:
            self.environment[node.identifier] += 1
            print(f"Incremented {node.identifier}, new value: {self.environment[node.identifier]}")

    def visit_DecrementNode(self, node):
        if isinstance(node.identifier, ArrayAccessNode):
            array = self.environment[node.identifier.name]
            index = self.visit(node.identifier.index)
            array[index] -= 1
            print(f"Decremented {node.identifier.name}[{index}], new value: {array[index]}")
        else:
            self.environment[node.identifier] -= 1
            print(f"Decremented {node.identifier}, new value: {self.environment[node.identifier]}")

    def visit_IfNode(self, node):
        condition_value = self.visit(node.condition)
        results = []
        if condition_value:
            for stmt in node.then_block:
                result = self.visit(stmt)
                if result is not None:
                    results.append(result)
        elif node.elif_blocks:
            for (cond, block) in node.elif_blocks:
                if self.visit(cond):
                    for stmt in block:
                        result = self.visit(stmt)
                        if result is not None:
                            results.append(result)
                    break
        if not condition_value and node.else_block:
            for stmt in node.else_block:
                result = self.visit(stmt)
                if result is not None:
                    results.append(result)
        return '\n'.join(map(str, results))  # Ensure all results are strings

    def visit_BinaryOperatorNode(self, node):
        left_val = self.visit(node.left)
        right_val = self.visit(node.right)
        print(f"Evaluating Binary Operator: {left_val} {node.operator} {right_val}")  # Debug print
        if node.operator == 'PLUS':
            return left_val + right_val
        elif node.operator == 'MINUS':
            return left_val - right_val
        elif node.operator == 'DIVIDE':
            return left_val / right_val
        elif node.operator == 'MULTIPLY':
            return left_val * right_val
        elif node.operator == 'EQUAL':
            return left_val == right_val
        elif node.operator == 'GREATER':
            return left_val > right_val
        elif node.operator == 'LESS':
            return left_val < right_val
        elif node.operator == 'GREATER_EQUAL':
            return left_val >= right_val
        elif node.operator == 'LESS_EQUAL':
            return left_val <= right_val
        elif node.operator == 'NOT_EQUAL':
            return left_val != right_val
        else:
            raise Exception(f"Unsupported operator {node.operator}")

    def visit_NumberNode(self, node):
        return node.value

    def visit_StringLiteralNode(self, node):
        return node.value

    def visit_CharacterNode(self, node):
        return node.value
    
    def visit_DoubleNode(self, node):
        return node.value

    def visit_VariableDeclarationNode(self, node):
        evaluated_expression = self.visit(node.expression)
        self.environment[node.name] = evaluated_expression
        print(f"Declared: {node.name} = {evaluated_expression}")
        return f"Variable '{node.name}' set to {evaluated_expression}"
    
    def visit_ArrayDeclarationNode(self, node):
        evaluated_elements = [self.visit(element) for element in node.elements]
        self.environment[node.name] = evaluated_elements
        print(f"Declared array: {node.name} = {evaluated_elements}")
        return f"Array '{node.name}' set to {evaluated_elements}"

    def visit_ArrayAccessNode(self, node):
        array = self.environment[node.name]
        index = self.visit(node.index)
        return array[index]

    def visit_ArrayAssignNode(self, node):
        array = self.environment.get(node.array_name)
        index = self.visit(node.index)
        value = self.visit(node.value)
        if array is not None and 0 <= index < len(array):
            array[index] = value
            print(f"Assigned {value} to {node.array_name}[{index}]")
        else:
            raise Exception(f"Array assignment out of bounds or array '{node.array_name}' not defined")

    def visit_OutputNode(self, node):
        output_value = self.visit(node.value)
        print(f"Output: {output_value}")
        return str(output_value)  # Ensure the output value is converted to a string

    def visit_AssignNode(self, node):
        self.environment[node.name] = self.visit(node.expression)
        return f"Variable {node.name} assigned value {self.environment[node.name]}"

    def visit_VariableAccessNode(self, node):
        if node.identifier in self.environment:
            return self.environment[node.identifier]
        else:
            raise Exception(f"Undefined variable {node.identifier}")

    def visit_FunctionCallNode(self, node):
        func = global_namespace.get(node.function_name)
        if func:
            args = [self.visit(arg) for arg in node.arguments]
            return func(*args)
        raise NameError(f"Function {node.function_name} not defined")

    def visit_list(self, node_list):
        results = [self.visit(node) for node in node_list if node]
        return ' '.join(map(str, results))  # Ensure all results are strings

    def no_visit_method(self, node):
        raise Exception(f'No visit_{type(node).__name__} method')

def run(code):
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    interpreter = Interpreter(parser)
    try:
        result = interpreter.interpret(ast)
        return result
    except Exception as e:
        print(f"Error during interpretation: {e}")
        return f'Error: {str(e)}'

if __name__ == "__main__":
    code = '''
array integer arr[8, 2, 3, 4, 5]
array string strArr["Hello", "World"]
while arr[0] < 10
    -> strArr[1]
    -> arr[0]
    arr[0]++
stop
'''
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    interpreter = Interpreter(parser)
    result = interpreter.interpret(ast)
    print(result)