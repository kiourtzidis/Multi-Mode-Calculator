from core.node import NumberNode, NegNode, AddNode, SubNode, MulNode, DivNode, FloorDivNode, ModNode, PowerNode, PostfixNode, VariableNode, FunctionNode

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

        while True:

            if self.peek() is None:
                break

            if self._is_multiplicand(self.peek()):
                lbp = 21
            else:
                lbp = self.lbp(self.peek())

            if self.peek().is_postfix_operator():
                token = self.advance()
                left = PostfixNode(left, token)
                continue

            if rbp >= lbp:
                break

            if self._is_multiplicand(self.peek()):
                right = self.parse_expression(21)
                left = MulNode(left, right)
                continue

            token = self.advance()
            left = self.led(token, left)

        return left


    def nud(self, token):
        if token is None:
            raise Exception('Unexpected end of input in nud')

        if token.is_number():
            return NumberNode(float(token.eval_value))

        if token.eval_value == '-':
            return NegNode(self.parse_expression(25))

        if token.is_left_parenthesis():
            expr = self.parse_expression(0)
            if not self.peek() or self.peek().eval_value != ')':
                raise Exception('Missing )')
            self.advance()
            return expr
        
        if token.is_abs():
            expr = self.parse_expression(0)

            if not self.peek() or self.peek().eval_value != '|':
                raise Exception('Missing closing |')

            self.advance()
            return FunctionNode('abs', expr)

        if token.is_variable() or token.is_constant():
            return VariableNode(token.eval_value)

        if token.is_function():
            if not self.peek() or not self.peek().is_left_parenthesis():
                raise Exception('Expected ( after function')

            self.advance()
            arg = self.parse_expression(0)

            if not self.peek() or not self.peek().is_right_parenthesis():
                raise Exception('Missing ) after function argument')

            self.advance()
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
            
        if token.is_postfix_operator():
            return PostfixNode(left, self.parse_expression(self.lbp(token)))

        raise Exception(f'Unexpected token in led: {token}')


    def lbp(self, token):

        if token.is_infix_operator():
            if token.eval_value in ('+', '-'):
                return 10
            if token.eval_value in ('*', '/', '//', '%'):
                return 20
            if token.eval_value == '**':
                return 30

        if token.is_postfix_operator():
            return 40

        return 0


    def _is_multiplicand(self, token):

        if token is None:
            return False

        return (
            token.is_value() or
            token.is_left_parenthesis() or
            token.is_variable() or
            token.is_function()
        ) 