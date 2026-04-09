import re
from .token import Token, TokenType

class Parser:

    def __init__(self):

        self.expression_pattern = re.compile(r'^[0-9x+\-*/().,^ a-zA-Z]+$')


    def parse(self, expression):

        tokens = self.tokenize(expression)

        display_expr = ''.join(t.display_value for t in tokens)
        eval_expr = ''.join(t.eval_value for t in tokens)

        return display_expr, eval_expr


    def tokenize(self, expression):

        expression = expression.replace(' ', '')

        if not self.expression_pattern.match(expression):
            raise ValueError('Error')

        tokens = []
        i = 0

        while i < len(expression):
            char = expression[i]

            if char.isdigit() or char == '.':
                num = char
                i += 1
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    num += expression[i]
                    i += 1
                tokens.append(Token(TokenType.NUMBER, num, num))
                continue

            if char in '+-*/^%':
                tokens.append(Token(TokenType.OPERATOR, char, '**' if char == '^' else char))
                i += 1
                continue

            if char in '()':
                tokens.append(Token(TokenType.PARENTHESIS, char, char))
                i += 1
                continue

            if char.isalpha():
                identifier = char
                i += 1
                while i < len(expression) and expression[i].isalpha():
                    identifier += expression[i]
                    i += 1

                if identifier == 'pi':
                    tokens.append(Token(TokenType.CONSTANT, 'π', 'pi'))
                elif identifier == 'e':
                    tokens.append(Token(TokenType.CONSTANT, 'e', 'e'))
                else:
                    tokens.append(Token(TokenType.FUNCTION, identifier, identifier))
                continue

            raise ValueError(f'Error')

        return tokens