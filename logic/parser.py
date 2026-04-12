from .node import NumberNode, NegNode, AddNode, SubNode, MulNode, DivNode, FloorDivNode, ModNode, FunctionNode

class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0


    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None


    def advance(self):
        token = self.peek()
        self.pos += 1
        return token


    def parse(self):
        return self.expression(0)


    def expression(self, rbp):
        token = self.advance()
        left = self.nud(token)

        while self.peek() and rbp < self.lbp(self.peek()):
            token = self.advance()
            left = self.led(token, left)

        return left


    def nud(self, token):
        if token.is_value():
            return NumberNode(float(token.eval_value))

        if token.display_value == '-':
            return NegNode(self.expression(100))

        if token.is_left_parenthesis():
            expr = self.expression(0)
            if not self.peek() or self.peek().display_value != ')':
                raise Exception('Missing )')
            self.advance()
            return expr

        if token.is_function():
            arg = self.expression(0)
            return FunctionNode(token.eval_value, arg)

        raise Exception(f'Unexpected token in nud: {token}')


    def led(self, token, left):

        if token.is_infix_operator():

            if token.display_value == '+':
                return AddNode(left, self.expression(10))

            if token.display_value == '-':
                return SubNode(left, self.expression(10))

            if token.display_value == '×':
                return MulNode(left, self.expression(20))

            if token.display_value == '÷':
                return DivNode(left, self.expression(20))

            if token.display_value == ' div ':
                return FloorDivNode(left, self.expression(20))

            if token.display_value == ' mod ':
                return ModNode(left, self.expression(20))

        raise Exception(f'Unexpected token in led: {token}')


    def lbp(self, token):
        if token.is_infix_operator():
            if token.display_value in ('+', '-'):
                return 10
            if token.display_value in ('×', '÷', ' div ', ' mod '):
                return 20
        return 0