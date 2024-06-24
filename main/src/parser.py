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
    StringLiteralNode,
    CharacterNode,
    OutputNode,
    VariableAccessNode
)

class SyntaxError(Exception):
    """Custom Syntax Error for parsing."""
    pass

class Parser:
    def __init__(self, tokens):
        self.tokens = iter(tokens)
        self.current_token = None
        self.next_token()

    def next_token(self):
        try:
            self.current_token = next(self.tokens)
        except StopIteration:
            self.current_token = None

    def expect(self, token_type):
        if self.current_token is not None and self.current_token[0] == token_type:
            token = self.current_token
            self.next_token()
            return token
        else:
            raise SyntaxError(f"Expected token type '{token_type}', but got '{self.current_token[0]}' instead.")

    def parse(self):
        ast = []
        while self.current_token is not None:
            if self.current_token[0] == 'OUTPUT':
                ast.append(self.parse_output())
            elif self.current_token[0].startswith('TYPE_'):
                ast.append(self.parse_variable_declaration())
            elif self.current_token[0] == 'IDENTIFIER' and self.peek() == 'COLON':
                ast.append(self.parse_assignment())
            elif self.current_token[0] == 'IDENTIFIER':
                ast.append(self.parse_variable_access())
            else:
                self.next_token()  # Skip unknown or unhandled tokens
        return ast

    def parse_variable_declaration(self):
        type_token = self.expect(self.current_token[0])[0]  # Get the type token
        identifier = self.expect('IDENTIFIER')[1]
        self.expect('COLON')
        
        # Depending on the type token, expect the correct literal type
        if 'STRING' in type_token:
            string_value = self.expect('STRING_LITERAL')[1]
            value = StringLiteralNode(string_value)
        elif 'INTEGER' in type_token:
            number_value = int(self.expect('NUMBER')[1])
            value = NumberNode(number_value)
        elif 'DOUBLE' in type_token:
            number_value = float(self.expect('FLOAT_LITERAL')[1])
            value = NumberNode(number_value)
        elif 'CHARACTER' in type_token:
            char_value = self.expect('CHARACTER_LITERAL')[1]
            value = CharacterNode(char_value) 
        else:
            print(f"Unsupported type {type_token}")  # Debug print
            raise SyntaxError("Unsupported type for variable declaration.")
        
        return VariableDeclarationNode(type_token[len('TYPE_'):].lower(), identifier, value)


    def parse_output(self):
        self.expect('OUTPUT')
        identifier = self.expect('IDENTIFIER')[1]
        return OutputNode(VariableAccessNode(identifier))

    def parse_variable_access(self):
        identifier = self.expect('IDENTIFIER')[1]
        return VariableAccessNode(identifier)

    def parse_assignment(self):
        identifier = self.expect('IDENTIFIER')[1]
        self.expect('COLON')
        value = self.parse_expression()
        return AssignNode(identifier, value)

    def parse_expression(self):
        # Simplified expression parsing for demonstration
        token = self.expect('NUMBER')
        return NumberNode(token[1])

    def peek(self):
        save_point = self.tokens
        next_token = next(save_point, None)
        self.tokens = save_point  # Restore the iterator's state
        return next_token[0] if next_token else None

# Example usage
