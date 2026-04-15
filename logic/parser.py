from .node import NumberNode, NegNode, AddNode, SubNode, MulNode, DivNode, FloorDivNode, ModNode, PowerNode, VariableNode, FunctionNode

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
        return self.parse_expression(0)


    def parse_expression(self, rbp):
        token = self.advance()
        if token is None:
            raise Exception('Unexpected end of input')
        left = self.nud(token)

        while self.peek():

            if self._is_multiplicand(self.peek()):
                left = MulNode(left, self.parse_expression(20))
                continue

            if rbp < self.lbp(self.peek()):
                token = self.advance()
                left = self.led(token, left)
                continue

            break

        return left


    def nud(self, token):
        if token is None:
            raise Exception('Unexpected end of input in nud')

        if token.is_value():
            return NumberNode(float(token.eval_value))

        if token.eval_value == '-':
            return NegNode(self.parse_expression(100))

        if token.is_left_parenthesis():
            expr = self.parse_expression(0)
            if not self.peek() or self.peek().eval_value != ')':
                raise Exception('Missing )')
            self.advance()
            return expr

        if token.is_variable():
            return VariableNode(token.eval_value)

        if token.is_function():
            arg = self.parse_expression(0)
            return FunctionNode(token.eval_value, arg)

        raise Exception(f'Unexpected token in nud: {token}')


    def led(self, token, left):

        if token is None:
            raise Exception('Unexpected end of tokens in led')

        if token.is_infix_operator():

            if token.eval_value == '+':
                return AddNode(left, self.parse_expression(self.lbp(token)))

            if token.eval_value == '-':
                return SubNode(left, self.parse_expression(self.lbp(token)))

            if token.eval_value == '*':
                return MulNode(left, self.parse_expression(self.lbp(token)))

            if token.eval_value == '/':
                return DivNode(left, self.parse_expression(self.lbp(token)))

            if token.eval_value == '//':
                return FloorDivNode(left, self.parse_expression(self.lbp(token)))

            if token.eval_value == '%':
                return ModNode(left, self.parse_expression(self.lbp(token)))
            
            if token.eval_value == '**':
                return PowerNode(left, self.parse_expression(self.lbp(token) - 1))

        raise Exception(f'Unexpected token in led: {token}')


    def lbp(self, token):
        if token.is_infix_operator():
            if token.eval_value in ('+', '-'):
                return 10
            if token.eval_value in ('*', '/', '//', '%'):
                return 20
            if token.eval_value == '**':
                return 30
        return 0


    def _is_multiplicand(self, token):

        if token is None:
            return False

        return (
            token.is_value() or
            token.is_left_parenthesis() or
            token.is_variable or
            token.is_function()
        ) 