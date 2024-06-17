class FunctionDeclaration:
    def __init__(self, name, parameters, body):
        # name: the name of the function as a string
        # parameters: a list of tuples, each tuple containing the type and name of the parameter
        # body: a list of statement nodes that make up the function body
        self.name = name
        self.parameters = parameters
        self.body = body

    def __repr__(self):
        # Provide a readable representation of the function for debugging
        return f"FunctionDeclaration(name={self.name}, parameters={self.parameters}, body={[str(stmt) for stmt in self.body]})"

class Node:
    """Base class for all nodes in the AST."""
    pass


class ForLoopNode:
    def __init__(self, variable, start, end, body):
        # variable: the loop counter variable
        # start: starting value of the loop counter
        # end: ending value of the loop counter
        # body: list of statements to execute in each iteration
        self.variable = variable
        self.start = start
        self.end = end
        self.body = body
        
    def __repr__(self):
        return f"ForLoopNode(variable={self.variable}, start={self.start}, end={self.end}, body={[str(stmt) for stmt in self.body]})"
    
class WhileLoopNode:
    def __init__(self, variable, end, body):
        # variable: the loop counter variable
        # end: ending condition for loop counter
        # body: list of statements to execute in each iteration
        self.variable = variable
        self.end = end
        self.body = body
        
    def __repr__(self):
        return f"WhileLoopNode(variable={self.variable}, end={self.end}, body={[str(stmt) for stmt in self.body]})"

class DoWhileNode(Node):
    """Node representing a 'do-while' loop in the AST."""
    def __init__(self, condition, body):
        # condition: the condition for while loop
        # body: list of statements to execute in each iteration
        self.condition = condition
        self.body = body

    def __repr__(self):
        return f"DoWhileNode(Condition: {self.condition}, Body: {self.body})"

        