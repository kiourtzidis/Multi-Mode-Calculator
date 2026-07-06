from core.node import NumberNode, NegNode, AddNode, SubNode, MulNode, DivNode, FloorDivNode, ModNode, PowerNode, PostfixNode, VariableNode, FunctionNode
from core.exceptions import SyntaxError

BP_ADDITIVE = 10
BP_MULTIPLICATIVE = 20
BP_IMPLICIT_MUL = 21
BP_POWER = 30
BP_POSTFIX = 40
BP_UNARY_NEG = 25

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
            raise SyntaxError('Unexpected end of input')

        left = self.nud(token)

        while True:
            next_token = self.peek()
            if next_token is None:
                break

            if self._is_multiplicand(next_token):
                if rbp >= BP_IMPLICIT_MUL:
                    break
                right = self.parse_expression(BP_IMPLICIT_MUL)
                left = MulNode(left, right)
                continue

            if next_token.is_postfix_operator():
                left = PostfixNode(left, self.advance())
                continue

            lbp = self.lbp(next_token)
            if rbp >= lbp:
                break

            left = self.led(self.advance(), left)

        return left


    def nud(self, token):

        if token.is_number():
            return NumberNode(float(token.eval_value))

        if token.eval_value == '-':
            return NegNode(self.parse_expression(BP_UNARY_NEG))

        if token.is_left_parenthesis():
            expr = self.parse_expression(0)
            if not self.peek() or self.peek().eval_value != ')':
                raise SyntaxError('Missing )')
            self.advance()
            return expr
        
        if token.is_abs():
            expr = self.parse_expression(0)

            if not self.peek() or self.peek().eval_value != '|':
                raise SyntaxError('Missing closing |')

            self.advance()
            return FunctionNode('abs', expr)

        if token.is_variable() or token.is_constant():
            return VariableNode(token.eval_value)

        if token.is_function():
            if not self.peek() or not self.peek().is_left_parenthesis():
                raise SyntaxError('Expected ( after function')

            self.advance()
            arg = self.parse_expression(0)

            if not self.peek() or not self.peek().is_right_parenthesis():
                raise SyntaxError('Missing ) after function argument')

            self.advance()
            return FunctionNode(token.eval_value, arg)

        raise SyntaxError(f'Unexpected token in nud: {token}')


    def led(self, token, left):

        if token is None:
            raise SyntaxError('Unexpected end of tokens in led')

        if token.is_infix_operator():

            if token.eval_value == '+':
                return AddNode(left, self.parse_expression(BP_ADDITIVE))

            if token.eval_value == '-':
                return SubNode(left, self.parse_expression(BP_ADDITIVE))

            if token.eval_value == '*':
                return MulNode(left, self.parse_expression(BP_MULTIPLICATIVE))

            if token.eval_value == '/':
                return DivNode(left, self.parse_expression(BP_MULTIPLICATIVE))

            if token.eval_value == '//':
                return FloorDivNode(left, self.parse_expression(BP_MULTIPLICATIVE))

            if token.eval_value == '%':
                return ModNode(left, self.parse_expression(BP_MULTIPLICATIVE))
            
            if token.eval_value == '**':
                return PowerNode(left, self.parse_expression(BP_POWER - 1))

        raise SyntaxError(f'Unexpected token in led: {token}')


    def lbp(self, token):

        if token.is_infix_operator():
            if token.eval_value in ('+', '-'):
                return BP_ADDITIVE
            if token.eval_value in ('*', '/', '//', '%'):
                return BP_MULTIPLICATIVE
            if token.eval_value == '**':
                return BP_POWER

        if token.is_postfix_operator():
            return BP_POSTFIX

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