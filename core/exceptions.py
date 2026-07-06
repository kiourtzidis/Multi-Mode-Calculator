class SyntaxError(Exception):

    def __init__(self, message='Invalid expression'):
        super().__init__(message)
        self.message = message


class MathError(Exception):

    def __init__(self, message='Math error'):
        super().__init__(message)
        self.message = message