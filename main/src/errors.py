class Error(Exception):
    """Base class for all errors in Quetzal."""
    def __init__(self, message):
        super().__init__(message)

class TypeError(Error):
    """Error thrown when a type mismatch occurs."""
    def __init__(self, message):
        super().__init__(f"Type error: {message}")

class IndexError(Error):
    """Error thrown when an index is out of the allowed range."""
    def __init__(self, message):
        super().__init__(f"Index error: {message}")

class NameError(Error):
    """Error thrown when referencing an undefined variable or function."""
    def __init__(self, message):
        super().__init__(f"Name error: {message}")
