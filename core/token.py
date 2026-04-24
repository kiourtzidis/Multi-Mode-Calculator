from enum import Enum, auto

class TokenType(Enum):
    NUMBER = auto()
    CONSTANT = auto()
    VARIABLE = auto()
    INFIX_OPERATOR = auto()
    POSTFIX_OPERATOR = auto()
    LPAREN = auto()
    RPAREN = auto()
    FUNCTION = auto()
    SPECIAL = auto()


class Token:

    def __init__(self, type, key, display_value, eval_value):

        self.type = type
        self.key = key
        self.display_value = display_value
        self.eval_value = eval_value


    def __eq__(self, other):

        if not isinstance(other, Token):
            return False

        return (
            self.type == other.type 
            and self.key == other.key 
            and self.display_value == other.display_value 
            and self.eval_value == other.eval_value
            )


    def __repr__(self):
        return f'Token({self.type}, {self.key}, {self.display_value}, {self.eval_value})'


    def is_number(self):
        return self.type == TokenType.NUMBER


    def is_constant(self):
        return self.type == TokenType.CONSTANT


    def is_value(self):
        return self.type in (TokenType.NUMBER, TokenType.CONSTANT)


    def is_left_parenthesis(self):
        return self.type == TokenType.LPAREN


    def is_right_parenthesis(self):
        return self.type == TokenType.RPAREN


    def is_infix_operator(self):
        return self.type == TokenType.INFIX_OPERATOR


    def is_postfix_operator(self):
        return self.type == TokenType.POSTFIX_OPERATOR


    def is_variable(self):
        return self.type == TokenType.VARIABLE


    def is_function(self):
        return self.type == TokenType.FUNCTION


    def is_special(self):
        return self.type == TokenType.SPECIAL