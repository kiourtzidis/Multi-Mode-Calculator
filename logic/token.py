from enum import Enum, auto

class TokenType(Enum):
    NUMBER = auto()
    CONSTANT = auto()
    OPERATOR = auto()
    PARENTHESIS = auto()
    FUNCTION = auto()


class Token:

    def __init__(self, type, display_value, eval_value):

        self.type = type
        self.display_value = display_value
        self.eval_value = eval_value


    def __eq__(self, other):

        if not isinstance(other, Token):
            return False

        return self.type == other.type and self.display_value == other.display_value and self.eval_value == other.eval_value


    def __repr__(self):
        return f'Token({self.type}, {self.display_value}, {self.eval_value})'