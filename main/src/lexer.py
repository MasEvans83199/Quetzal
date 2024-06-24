import re

class Lexer:
    def __init__(self, source_code):
        self.tokens = []
        self.source_code = source_code.lower()

    def tokenize(self):
        patterns = {
            'TYPE_STRING': r'\bstring\b',
            'TYPE_INTEGER': r'\binteger\b',
            'TYPE_DOUBLE': r'\bdouble\b',
            'TYPE_CHARACTER': r'\bcharacter\b',
            'STRING_LITERAL': r'"[^"]*"',
            'FLOAT_LITERAL': r'\b\d+\.\d+\b',
            'NUMBER': r'\b\d+\b',
            'CHARACTER_LITERAL': r"'.'",
            'FUN': r'\bfun\b',
            'IDENTIFIER': r'\b[a-zA-Z_][a-zA-Z0-9_]*\b',  # This will not match any reserved keyword due to above explicit definitions
            'COLON': r':',
            'OUTPUT': r'->',
            # Other tokens...
            'PLUS': r'\+',
            'MINUS': r'-',
            'DIVIDE': r'/',
            'STOP': r'\bstop\b',
            'COMMA': r',',
            'OPEN_PAREN': r'\(',
            'CLOSE_PAREN': r'\)',
            'OPEN_BRACE': r'\{',
            'CLOSE_BRACE': r'\}',
            'EQUAL': r':=',
            'GREATER': r':>',
            'LESS': r':<',
            'GREATER_EQUAL': r':?>',
            'LESS_EQUAL': r':?<',
            'NOT_EQUAL': r':!',
            'AND': r':&',
            'OR': r':\|',
            'THEN': r'::>',
            'INCREMENT': r'\+\+',
            'DECREMENT': r'--',
            'PLUS_EQUAL': r':\+',
            'MINUS_EQUAL': r':-',
            'FOR': r'\bfor\b',
            'WHILE': r'\bwhile\b',
            'FROM': r'\bfrom\b',
            'TO': r'\bto\b',
            'ENQUEUE': r'\benqueue\b',
            'DEQUEUE': r'\bdequeue\b',
            'POP': r'\bpop\b',
            'PUSH': r'\bpush\b',
            'PEEK': r'\bpeek\b',
            'POP_BACK': r'\bpop_back\b',
            'PUSH_BACK': r'\bpush_back\b',
            'IF': r'\bif\b',
            'ELSE_IF': r'\belif\b',
            'DO': r'\bdo\b',
        }

        # We go line by line to avoid any confusion with multi-line inputs
        for line in self.source_code.split('\n'):
            position = 0
            while position < len(line):
                match = None
                for token_type, pattern in patterns.items():
                    regex = re.compile(pattern)
                    match = regex.match(line, position)
                    if match:
                        self.tokens.append((token_type, match.group()))
                        print(f"Generated Token: {token_type}, Value: {match.group()}")
                        position = match.end()  # Move position past the end of the matched token
                        break
                if not match:
                    position += 1  # If no token matched, increment to avoid infinite loop
        return self.tokens

# Example usage
if __name__ == "__main__":
    code = 'string str : "Hello world"'
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    print(tokens)  # Output tokens for review
