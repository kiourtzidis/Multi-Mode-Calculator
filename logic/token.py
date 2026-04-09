from enum import Enum

class TokenType(Enum):
    NUMBER = 1
    CONSTANT = 2
    OPERATOR = 3
    PARENTHESIS = 4
    FUNCTION = 5


class Token:

    def __init__(self, type, display_value, eval_value):

        self.type = type
        self.display_value = display_value
        self.eval_value = eval_value


    def __repr__(self):
        return f'Token({self.type}, {self.display_value}, {self.eval_value})'