from lexer import Lexer
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
    DoubleNode,
    ArrayDeclarationNode,
    ArrayAccessNode,
    ArrayAssignNode,
    ExpressionNode,
    OutputNode,
    VariableAccessNode,
    IncrementNode,
    DecrementNode,
    StopNode
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
            if self.current_token[0] == 'IF':
                ast.append(self.parse_if_statement())
            elif self.current_token[0] == 'FOR':
                ast.append(self.parse_for_loop())
            elif self.current_token[0] == 'WHILE':  # Correct token checking for WHILE
                ast.append(self.parse_while_loop())
            elif self.current_token[0] == 'DO':
                ast.append(self.parse_do_while_loop())
            elif self.current_token[0].startswith('TYPE_'):
                ast.append(self.parse_variable_declaration())
            elif self.current_token[0] == 'ARRAY':
                ast.append(self.parse_array_declaration())
            elif self.current_token[0] == 'OUTPUT':
                ast.append(self.parse_output())
            elif self.current_token[0] == 'IDENTIFIER' and self.peek() == 'COLON':
                ast.append(self.parse_assignment())
            elif self.current_token[0] == 'IDENTIFIER':
                ast.append(self.parse_variable_access())
            else:
                self.next_token()  # Skip unknown or unhandled tokens
        return ast

    def parse_variable_declaration(self):
        if self.current_token[0] == 'ARRAY':
            self.expect('ARRAY')
            array_type = self.expect(self.current_token[0])[1]
            name = self.expect('IDENTIFIER')[1]
            self.expect('SQUARE_OPEN')
            elements = []
            while self.current_token[0] != 'SQUARE_CLOSE':
                if self.current_token[0] in ['NUMBER', 'STRING_LITERAL', 'CHARACTER_LITERAL']:
                    elements.append(self.parse_primary_expression())
                if self.current_token[0] == 'COMMA':
                    self.next_token()
            self.expect('SQUARE_CLOSE')
            return ArrayDeclarationNode(array_type, name, elements)
        else:
            type_token = self.expect(self.current_token[0])[0]
            identifier = self.expect('IDENTIFIER')[1]
            self.expect('COLON')
            expression = self.parse_expression()
            return VariableDeclarationNode(type_token[len('TYPE_'):].lower(), identifier, expression)
    
    def parse_array_declaration(self):
        self.expect('ARRAY')
        type_token = self.expect(self.current_token[0])[0]
        identifier = self.expect('IDENTIFIER')[1]
        self.expect('SQUARE_OPEN')
        elements = []
        while self.current_token[0] != 'SQUARE_CLOSE':
            elements.append(self.parse_expression())
            if self.current_token[0] == 'COMMA':
                self.next_token()
        self.expect('SQUARE_CLOSE')
        return ArrayDeclarationNode(type_token[len('TYPE_'):].lower(), identifier, elements)
    
    def parse_array_access(self, identifier):
        self.expect('SQUARE_OPEN')
        index = self.parse_expression()
        self.expect('SQUARE_CLOSE')
        if self.current_token[0] == 'INCREMENT':
            self.next_token()
            return IncrementNode(ArrayAccessNode(identifier, index))
        elif self.current_token[0] == 'DECREMENT':
            self.next_token()
            return DecrementNode(ArrayAccessNode(identifier, index))
        return ArrayAccessNode(identifier, index)

    def parse_output(self):
        self.expect('OUTPUT')
        if self.current_token[0] == 'IDENTIFIER':
            identifier = self.expect('IDENTIFIER')[1]
            if self.current_token and self.current_token[0] == 'SQUARE_OPEN':
                self.expect('SQUARE_OPEN')
                index = self.parse_expression()
                self.expect('SQUARE_CLOSE')
                return OutputNode(ArrayAccessNode(identifier, index))
            return OutputNode(VariableAccessNode(identifier))
        elif self.current_token[0] == 'STRING_LITERAL':
            string = self.expect('STRING_LITERAL')[1]
            return OutputNode(StringLiteralNode(string))
        elif self.current_token[0] == 'CHARACTER_LITERAL':
            char = self.expect('CHARACTER_LITERAL')[1]
            return OutputNode(CharacterNode(char))
        else:
            raise SyntaxError(f"Unexpected token {self.current_token[0]} in output")

    def parse_variable_access(self):
        identifier = self.expect('IDENTIFIER')[1]
        return VariableAccessNode(identifier)

    def parse_assignment(self):
        identifier = self.expect('IDENTIFIER')[1]
        if self.current_token and self.current_token[0] == 'SQUARE_OPEN':
            self.expect('SQUARE_OPEN')
            index = self.parse_expression()
            self.expect('SQUARE_CLOSE')
            self.expect('COLON')
            value = self.parse_expression()
            return ArrayAssignNode(identifier, index, value)
        self.expect('COLON')
        value = self.parse_expression()
        return AssignNode(identifier, value)

    def parse_if_statement(self):
        self.expect('IF')
        condition = self.parse_expression()
        self.expect('THEN')
        then_block = self.parse_block()

        elif_blocks = []
        while self.current_token and self.current_token[0] == 'ELSE_IF':
            self.expect('ELSE_IF')
            elif_condition = self.parse_expression()
            self.expect('THEN')
            elif_block = self.parse_block()
            elif_blocks.append((elif_condition, elif_block))

        else_block = None
        if self.current_token and self.current_token[0] == 'ELSE':
            self.expect('ELSE')
            self.expect('THEN')
            else_block = self.parse_block()

        return IfNode(condition, then_block, elif_blocks, else_block)

    def parse_for_loop(self):
        self.expect('FOR')
        if self.current_token[0].startswith('TYPE_'):
            declaration = self.parse_variable_declaration()
            identifier = declaration.name
        else:
            identifier = self.expect('IDENTIFIER')[1]
        self.expect('TO')
        end_value = self.parse_expression()
        body = self.parse_block()
        if isinstance(declaration, VariableDeclarationNode):
            return [declaration, ForLoopNode(identifier, end_value, body)]
        return ForLoopNode(identifier, end_value, body)
    
    def parse_while_loop(self):
        self.expect('WHILE')
        condition = self.parse_expression()
        print(f"Parsed WHILE condition: {condition}")
        body = self.parse_block()
        print(f"Parsed WHILE body: {body}")
        return WhileLoopNode(condition, body)
    
    def parse_do_while_loop(self):
        self.expect('DO')
        body = self.parse_block()
        self.expect('WHILE')
        condition = self.parse_expression()
        print(f"Parsed DO-WHILE body: {body}")
        print(f"Parsed DO-WHILE condition: {condition}")
        return DoWhileNode(body, condition)

    def parse_block(self):
        block = []
        self.expect('INDENT')
        while self.current_token and self.current_token[0] != 'DEDENT':
            if self.current_token[0] == 'INCREMENT':
                self.next_token()  # Consume the INCREMENT token
                identifier = self.expect('IDENTIFIER')[1]
                block.append(IncrementNode(identifier))
            elif self.current_token[0] == 'DECREMENT':
                self.next_token()  # Consume the DECREMENT token
                identifier = self.expect('IDENTIFIER')[1]
                block.append(DecrementNode(identifier))
            elif self.current_token[0] == 'OUTPUT':
                block.append(self.parse_output())
            elif self.current_token[0].startswith('TYPE_') or self.current_token[0] == 'ARRAY':
                block.append(self.parse_variable_declaration())
            elif self.current_token[0] == 'IDENTIFIER':
                identifier = self.expect('IDENTIFIER')[1]
                if self.current_token[0] == 'SQUARE_OPEN':
                    block.append(self.parse_array_access(identifier))
                else:
                    block.append(VariableAccessNode(identifier))
            else:
                block.append(self.parse_expression())
        self.expect('DEDENT')
        return block

    def parse_expression(self):
        expr = self.parse_primary_expression()

        while self.current_token and self.current_token[0] in ['PLUS', 'MINUS', 'DIVIDE', 'MULTIPLY', 'GREATER', 'LESS', 'GREATER_EQUAL', 'LESS_EQUAL', 'EQUAL']:
            operator = self.current_token[0]
            self.next_token()
            right = self.parse_primary_expression()
            expr = BinaryOperatorNode(expr, operator, right)

        return expr

    def parse_primary_expression(self):
        if self.current_token[0] == 'IDENTIFIER':
            identifier = self.expect('IDENTIFIER')[1]
            if self.current_token and self.current_token[0] == 'SQUARE_OPEN':
                self.expect('SQUARE_OPEN')
                index = self.parse_expression()
                self.expect('SQUARE_CLOSE')
                return ArrayAccessNode(identifier, index)
            if self.current_token and self.current_token[0] == 'INCREMENT':
                self.next_token()  # Consume the INCREMENT token
                return IncrementNode(identifier)
            elif self.current_token and self.current_token[0] == 'DECREMENT':
                self.next_token()  # Consume the DECREMENT token
                return DecrementNode(identifier)
            return VariableAccessNode(identifier)
        elif self.current_token[0] == 'NUMBER':
            number = int(self.expect('NUMBER')[1])
            return NumberNode(number)
        elif self.current_token[0] == 'FLOAT_LITERAL':
            float_number = float(self.expect('FLOAT_LITERAL')[1])
            return DoubleNode(float_number)
        elif self.current_token[0] == 'STRING_LITERAL':
            string = self.expect('STRING_LITERAL')[1]
            return StringLiteralNode(string)
        elif self.current_token[0] == 'CHARACTER_LITERAL':
            char = self.expect('CHARACTER_LITERAL')[1]
            return CharacterNode(char)
        else:
            raise SyntaxError(f"Unexpected token type {self.current_token[0]}")

    def peek(self):
        save_point = self.tokens
        next_token = next(save_point, None)
        self.tokens = save_point
        return next_token[0] if next_token else None


if __name__ == "__main__":
    code = '''integer int : 10
do
    -> int
    int--
while int :> 5
stop
'''
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()
    print("AST:", ast)  # Output AST for review