from ast import FunctionDeclaration, ForLoopNode, WhileLoopNode, DoWhileNode

class Parser:
    def __init__(self, tokens):
        # Initialize the parser with a list of tokens
        self.tokens = iter(tokens)
        self.current_token = None
        self.next_token()  # Initialize the first token

    def next_token(self):
        # Move to the next token in the list, or None if at the end
        self.current_token = next(self.tokens, None)

    def parse_function(self):
        # Parse a function definition, starting from the 'FUN' token
        assert self.current_token.type == 'FUN', "Function must start with 'fun'"
        self.next_token()  # Move past 'FUN'
        function_name = self.expect('IDENTIFIER').value  # Expect function name next
        self.expect('OPEN_PAREN')  # Function parameters start with '('
        parameters = self.parse_parameters()  # Parse all parameters
        self.expect('CLOSE_PAREN')  # Parameters end with ')'
        body = self.parse_statements()  # Parse all statements in the function body
        self.expect('STOP')  # Function body ends with 'stop'
        return FunctionDeclaration(function_name, parameters, body)  # Return a function declaration node

    def parse_parameters(self):
        # Parse parameters within the function definition
        parameters = []
        while self.current_token.type != 'CLOSE_PAREN':
            param_type = self.expect('TYPE').value  # Expect a type identifier (INTEGER, STRING, etc.)
            param_name = self.expect('IDENTIFIER').value  # Expect the parameter's name
            parameters.append((param_type, param_name))  # Add parameter tuple to list
            if self.current_token.type == 'COMMA':
                self.next_token()  # Skip over commas between parameters
        return parameters  # Return the list of parsed parameters

    def parse_statements(self):
        # Parse statements inside the function body
        statements = []
        while self.current_token.type != 'STOP':
            statement = self.parse_statement()  # Parse a single statement
            statements.append(statement)  # Add the parsed statement to the list
        return statements  # Return the list of statements
    
    def parse_for_loop(self):
        # Expect the 'for' keyword
        self.expect('FOR')
        variable = self.expect('IDENTIFIER').value  # The loop variable
        self.expect('FROM')
        start = self.parse_expression()  # Starting value
        self.expect('TO')
        end = self.parse_expression()  # Ending value

        # Now parse the body of the loop
        body = []
        while self.current_token.type != 'STOP':
            body.append(self.parse_statement())

        self.expect('STOP')  # End of the loop body
        return ForLoopNode(variable, start, end, body)
    
    def parse_comparison_operator(self):
        if self.current_token.type in ['LESS', 'GREATER', 'LESS_EQUAL', 'GREATER_EQUAL', 'EQUAL', 'NOT_EQUAL']:
            operator = self.current_token.type
            self.next_token()  # Move past the operator
            return operator
        else:
            raise SyntaxError(f"Expected a comparison operator, found '{self.current_token.type}'")

    def parse_while_loop(self):
        self.expect('WHILE')  # Assume you start with the 'WHILE' keyword
        variable = self.expect('IDENTIFIER').value  # Get the loop variable

        operator = self.parse_comparison_operator()  # Parse the comparison operator

        comparison_value = self.parse_expression()  # Parse the value to compare against

        # Now parse the body of the loop
        body = []
        while self.current_token.type != 'STOP':
            body.append(self.parse_statement())

        self.expect('STOP')  # End of the loop body
        return WhileLoopNode(variable, operator, comparison_value, body)
    
    def parse_do_while(self):
        """Parse a do-while loop statement."""
        self.expect('DO')
        self.expect('OPEN_BRACE')
        body = self.parse_statements()  # Method that parses multiple statements within braces
        self.expect('CLOSE_BRACE')
        self.expect('WHILE')
        condition = self.parse_expression()  # Method that parses the condition expression

        return DoWhileNode(condition, body)


    def expect(self, type):
        # Ensure the current token matches the expected type
        if self.current_token.type == type:
            token = self.current_token
            self.next_token()  # Move past the token after matching
            return token
        else:
            raise SyntaxError(f"Expected {type}, but got {self.current_token.type}")
