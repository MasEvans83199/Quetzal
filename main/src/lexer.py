import re

class Lexer:
    def __init__(self, source_code):
        self.tokens = []
        self.source_code = source_code
        self.indent_stack = [0]  # Start with an initial indent level of 0

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
            'IF': r'\bif\b',
            'ELSE_IF': r'\belse_if\b',
            'ELSE': r'\belse\b',
            'THEN': r'\bthen\b',
            'STOP': r'\bstop\b',
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
            'DO': r'\bdo\b',
            'UNTIL': r'\buntil\b',
            'NEW_LINE': r'\n',
            'IDENTIFIER': r'\b[a-zA-Z_][a-zA-Z0-9_]*\b',
            'INCREMENT': r'\+\+',
            'DECREMENT': r'--',
            'PLUS_EQUAL': r':\+',
            'MINUS_EQUAL': r':-',
            'EQUAL': r':=',
            'GREATER': r'>',
            'LESS': r'<',
            'GREATER_EQUAL': r':>',
            'LESS_EQUAL': r':<',
            'NOT_EQUAL': r':!',
            'AND': r':&',
            'OR': r':\|',
            'COLON': r':',
            'OUTPUT': r'->',
            'PLUS': r'\+',
            'MINUS': r'-',
            'DIVIDE': r'/',
            'MULTIPLY': r'\*',
            'COMMA': r',',
            'OPEN_PAREN': r'\(',
            'CLOSE_PAREN': r'\)',
            'OPEN_BRACE': r'\{',
            'CLOSE_BRACE': r'\}',
        }

        for line in self.source_code.split('\n'):
            position = 0
            current_indent = len(line) - len(line.lstrip())
            previous_indent = self.indent_stack[-1]

            if current_indent > previous_indent:
                self.indent_stack.append(current_indent)
                self.tokens.append(('INDENT', ' ' * current_indent))
            while current_indent < previous_indent:
                self.indent_stack.pop()
                previous_indent = self.indent_stack[-1]
                self.tokens.append(('DEDENT', ''))

            while position < len(line):
                match = None
                for token_type, pattern in patterns.items():
                    regex = re.compile(pattern)
                    match = regex.match(line, position)
                    if match:
                        self.tokens.append((token_type, match.group()))
                        print(f"Generated Token: {token_type}, Value: '{match.group()}'")
                        position = match.end()
                        break
                if not match:
                    print(f"No match at position {position} in line: {line}")
                    position += 1
        return self.tokens

# Example usage
if __name__ == "__main__":
    code = '''integer int : 0
integer limit : 5
while int < limit
    -> int
    int++
stop
'''
    lexer = Lexer(code)
    tokens = lexer.tokenize()
    print(tokens)  # Output tokens for review
