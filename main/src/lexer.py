import re

class Lexer:
    def __init__(self, source_code):
        self.tokens = []  # List of tokens
        self.source_code = source_code.lower()  # Convert source to lowercase for case insensitivity

    def tokenize(self):
        tokens_re = {
            'FUN': r'\bfun\b',  # Matches the 'fun' keyword for function definitions
            'IDENTIFIER': r'\b[a-zA-Z_][a-zA-Z0-9_]*\b',  # Matches identifiers
            'COLON': r':',  # Matches the colon symbol used in variable typing and assignment
            'INTEGER': r'\binteger\b',  # Matches the 'integer' type keyword
            'STRING': r'\bstring\b',  # Matches the 'string' type keyword
            'DOUBLE': r'\bdouble\b',  # Matches the 'double' type keyword
            'CHARACTER': r'\bcharacter\b',  # Matches the 'character' type keyword
            'NUMBER': r'\b\d+\b',  # Matches integers
            'FLOAT': r'\b\d+\.\d+\b',  # Matches floating-point numbers
            'PLUS': r'\+',  # Matches the plus operator
            'MINUS': r'-',  # Matches the minus operator
            'DIVIDE': r'/',  # Matches the division operator
            'OUTPUT': r'->',  # Matches the output operator '->'
            'STOP': r'\bstop\b',  # Matches the 'stop' keyword
            'COMMA': r',',  # Matches commas for separating parameters
            'OPEN_PAREN': r'\(',  # Matches open parentheses
            'CLOSE_PAREN': r'\)',  # Matches close parentheses
            'COMPARATOR': r':?', # Matches comparisons
            'GREATER_THAN': r':>', # Matches greater-than operator
            'LESS_THAN': r':<', # Matches less-than operator
            'GREATER_EQUAL': r':?>', # Matches greater-than equal to operator
            'LESS_EQUAL': r':?<', # Matches less-than equal to operator
            'NOT_EQUAL': r':!', # Matches not equal to operator
            'AND': r':&', # Matches operator 'and'
            'OR': r':|', # Matches operator 'or'
            'THEN': r'::>', # Matches operator 'then'
            'INCREMENT': r'++', # Matches increment operator
            'DECREMENT': r'--', # Matches decrement operator
            'PLUS_EQUAL': r':+', # Matches plus-equal operator
            'MINUS_EQUAL': r':-', # Matches minus-equal operator
            
        }

        for line in self.source_code.split('\n'):
            for token_type, reg_ex in tokens_re.items():
                for match in re.finditer(reg_ex, line):
                    self.tokens.append((token_type, match.group()))

        return self.tokens
