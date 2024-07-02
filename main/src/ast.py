class Node:
    """Base class for all AST nodes."""
    pass

class FunctionDeclaration(Node):
    """Represents a function declaration."""
    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters
        self.body = body

class IfNode(Node):
    """Represents an 'if' statement with optional 'elif' and 'else' blocks."""
    def __init__(self, condition, then_block, elif_blocks, else_block):
        self.condition = condition
        self.then_block = then_block
        self.elif_blocks = elif_blocks
        self.else_block = else_block

class WhileLoopNode(Node):
    """Represents a 'while' loop."""
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

class DoWhileNode(Node):
    """Represents a 'do-while' loop."""
    def __init__(self, body, condition):
        self.body = body
        self.condition = condition
        
class ForLoopNode:
    def __init__(self, identifier, end_value, body):
        self.identifier = identifier
        self.end_value = end_value
        self.body = body

class BinaryOperatorNode(Node):
    """Represents a binary operation (e.g., addition, subtraction)."""
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class NumberNode(Node):
    """Represents a numeric literal."""
    def __init__(self, value):
        self.value = value

class VariableDeclarationNode(Node):
    """Represents a variable declaration."""
    def __init__(self, type_name, name, expression):
        self.type_name = type_name
        self.name = name
        self.expression = expression

class AssignNode(Node):
    """Represents an assignment to a variable."""
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

class FunctionCallNode(Node):
    """Represents a function call."""
    def __init__(self, function_name, arguments):
        self.function_name = function_name
        self.arguments = arguments
        
class StringLiteralNode(Node):
    def __init__(self,value):
        self.value = value.strip('"')
        
class CharacterNode(Node):
    """Represents a character literal."""
    def __init__(self, value):
        # Ensure the character is stored without surrounding quotes
        self.value = value.strip("'")
        
class DoubleNode(Node):
    """Represents a double literal"""
    def __init__(self, value):
        self.value = value
        
    def __repr__(self):
        return f'DoubleNode(value={self.value})'
        
class ExpressionNode(Node):
    def __init__(self, left, operator=None, right=None):
        self.left = left
        self.operator = operator
        self.right = right
        
class IncrementNode(Node):
    def __init__(self, identifier):
        self.identifier = identifier
        
class DecrementNode(Node):
    def __init__(self, identifier):
        self.identifier = identifier

class StopNode(Node):
    pass

class OutputNode(Node):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"OutputNode(value={self.value})"

class VariableAccessNode:
    def __init__(self, identifier):
        self.identifier = identifier

    def __repr__(self):
        return f"VariableAccessNode(identifier='{self.identifier}')"
