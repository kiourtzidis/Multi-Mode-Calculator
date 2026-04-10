import re
from .token import Token, TokenType

class Parser:

    def __init__(self):

        self.expression_pattern = re.compile(r'^[0-9+\-*/^().,%|!a-zA-Z×÷πʸ²³⁻¹√∛‰]*$')
        self.token_map = {
            '+': (TokenType.OPERATOR, '+', '+'),
            '-': (TokenType.OPERATOR, '-', '-'),
            '×': (TokenType.OPERATOR, '×', '*'),
            '÷': (TokenType.OPERATOR, '÷', '/'),
            'div': (TokenType.OPERATOR, ' div ', '//'),
            'mod': (TokenType.OPERATOR, ' mod ', '%'),

            '(': (TokenType.PARENTHESIS, '(', '('),
            ')': (TokenType.PARENTHESIS, ')', ')'),

            'sin': (TokenType.FUNCTION, 'sin(', 'sin('),
            'cos': (TokenType.FUNCTION, 'cos(', 'cos('),
            'tan': (TokenType.FUNCTION, 'tan(', 'tan('),
            'cot': (TokenType.FUNCTION, 'cot(', 'cot('),
            'sin⁻¹': (TokenType.FUNCTION, 'sin⁻¹(', 'arcsin('),
            'cos⁻¹': (TokenType.FUNCTION, 'cos⁻¹(', 'arccos('),
            'tan⁻¹': (TokenType.FUNCTION, 'tan⁻¹(', 'arctan('),
            'cot⁻¹': (TokenType.FUNCTION, 'cot⁻¹(', 'arccot('),

            'log': (TokenType.FUNCTION, 'log(', 'log10('),
            'ln': (TokenType.FUNCTION, 'ln(', 'log('),
            '%': (TokenType.OPERATOR, '%', '*(1/100)'),
            'log₂': (TokenType.FUNCTION, 'log₂(', 'log2('),
            '‰': (TokenType.OPERATOR, '‰', '*(1/1000)'),

            'x²': (TokenType.OPERATOR, '²', '**(2)'),
            'x³': (TokenType.OPERATOR, '³', '**(3)'),
            'xʸ': (TokenType.OPERATOR, '^', '**'),
            'x⁻¹': (TokenType.OPERATOR, '⁻¹', '**(-1)'),
            '√': (TokenType.FUNCTION, '√(', 'sqrt('),
            '∛': (TokenType.FUNCTION, '∛(', 'cbrt('),
            '×10ʸ': (TokenType.FUNCTION, '×10^', '*10**'),

            'π': (TokenType.CONSTANT, 'π', 'pi'),
            'e': (TokenType.CONSTANT, 'e', 'e'),

            'round': (TokenType.FUNCTION, 'round(', 'round('),
            'floor': (TokenType.FUNCTION, 'floor(', 'floor('),
            'ceil': (TokenType.FUNCTION, 'ceil(', 'ceil('),
            'trunc': (TokenType.FUNCTION, 'trunc(', 'trunc('),
            'frac': (TokenType.FUNCTION, 'frac(', 'frac('),
            'sign': (TokenType.FUNCTION, 'sign(', 'sign('),
            'gamma': (TokenType.FUNCTION, 'gamma(', 'gamma('),
            'lgamma': (TokenType.FUNCTION, 'lgamma(', 'lgamma('),
            'csc': (TokenType.FUNCTION, 'csc(', 'csc('),
            'sec': (TokenType.FUNCTION, 'sec(', 'sec('),
            'csc⁻¹': (TokenType.FUNCTION, 'csc⁻¹(', 'arccsc('),
            'sec⁻¹': (TokenType.FUNCTION, 'sec⁻¹(', 'arcsec('),
            'sinh': (TokenType.FUNCTION, 'sinh(', 'sinh('),
            'cosh': (TokenType.FUNCTION, 'cosh(', 'cosh('),
            'tanh': (TokenType.FUNCTION, 'tanh(', 'tanh('),
            'csch': (TokenType.FUNCTION, 'csch(', 'csch('),
            'sech': (TokenType.FUNCTION, 'sech(', 'sech('),
            'coth': (TokenType.FUNCTION, 'coth(', 'coth('),
            'sinh⁻¹': (TokenType.FUNCTION, 'sinh⁻¹(', 'arcsinh('),
            'cosh⁻¹': (TokenType.FUNCTION, 'cosh⁻¹(', 'arccosh('),
            'tanh⁻¹': (TokenType.FUNCTION, 'tanh⁻¹(', 'arctanh('),
            'csch⁻¹': (TokenType.FUNCTION, 'csch⁻¹(', 'arccsch('),
            'sech⁻¹': (TokenType.FUNCTION, 'sech⁻¹(', 'arcsech('),
            'coth⁻¹': (TokenType.FUNCTION, 'coth⁻¹(', 'arccoth('),

            # Need Special Handling
            '!': (TokenType.OPERATOR, '!', '!'),
            '|': (TokenType.FUNCTION, '|', 'abs('),
            'Ans': (TokenType.NUMBER, 'Ans', 'Ans'),

            # For Graph Mode
            '10ˣ': (TokenType.FUNCTION, '10ˣ', '10**'),
            '2ˣ': (TokenType.FUNCTION, '2ˣ', '2**'),
            'eˣ': (TokenType.FUNCTION, 'eˣ', 'exp(x)'),
        }


    def parse(self, expression):

        tokens = self.tokenize(expression)

        display_expr = ''.join(token.display_value for token in tokens)
        eval_expr = ''.join(token.eval_value for token in tokens)

        return display_expr, eval_expr


    def tokenize(self, expression):

        expression = expression.replace(' ', '')

        if not self.expression_pattern.match(expression):
            raise ValueError('Error')

        tokens = []
        i = 0
        abs_open = False

        sorted_keys = sorted(self.token_map.keys(), key=len, reverse=True)

        while i < len(expression):

            matched = False
            for key in sorted_keys:
                if expression.startswith(key, i):

                    token_type, display_str, eval_str = self.token_map[key]

                    if key == '|':
                        if not abs_open:
                            tokens.append(Token(TokenType.FUNCTION, '|', 'abs('))
                            abs_open = True
                        else:
                            tokens.append(Token(TokenType.PARENTHESIS, '|', ')'))
                            abs_open = False
                    else:
                        tokens.append(Token(token_type, display_str, eval_str))

                    i += len(key)
                    matched = True
                    break

            if matched:
                continue

            char = expression[i]

            if char.isdigit() or char == '.':
                num = char
                i += 1

                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    num += expression[i]
                    i += 1

                tokens.append(Token(TokenType.NUMBER, num, num))
                continue

            if char.isalpha():
                identifier = char
                i += 1

                while i < len(expression) and expression[i].isalnum():
                    identifier += expression[i]
                    i += 1

                if identifier in self.token_map:
                    token_type, display_str, eval_str = self.token_map[identifier]
                    tokens.append(Token(token_type, display_str, eval_str))
                else:
                    raise ValueError('Error')

                continue

            raise ValueError('Error')

        return tokens