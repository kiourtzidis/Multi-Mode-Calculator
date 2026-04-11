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
            return ('num', float(token.eval_value))
        
        if token.is_left_parenthesis():
            expr = self.expression(0)
            if not self.peek() or self.peek().display_value != ')':
                raise Exception('Missing )')
            self.advance()
            return expr
        
        if token.display_value == '-':
            return ('neg', self.expression(100))
        
        raise Exception(f'Unexpected token in nud: {token}')
    

    def led(self, token, left):
        if token.is_infix_operator():

            if token.display_value in ('+', '-'):
                return (token.eval_value, left, self.expression(10))
            if token.display_value in ('×', '÷', ' div ', ' mod '):
                return (token.eval_value, left, self.expression(20))

        raise Exception(f'Unexpected token in led: {token}')
    

    def lbp(self, token):
        if token.is_infix_operator():
            if token.display_value in ('+', '-'):
                return 10
            if token.display_value in ('×', '÷', ' div ', ' mod '):
                return 20
        return 0
    

def evaluate(node):

    if node[0] == 'num':
         return node[1]

    if node[0] == 'neg':
        return -evaluate(node[1])

    if node[0] == '+':
        return evaluate(node[1]) + evaluate(node[2])

    if node[0] == '-':
        return evaluate(node[1]) - evaluate(node[2])

    if node[0] == '*':
        return evaluate(node[1]) * evaluate(node[2])

    if node[0] == '/':
        return evaluate(node[1]) / evaluate(node[2])
    
    if node[0] == '//':
        return evaluate(node[1]) // evaluate(node[2])

    if node[0] == '%':
        return evaluate(node[1]) % evaluate(node[2])
    
    raise Exception(f'Unknown node: {node}')