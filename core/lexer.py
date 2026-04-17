import re
from core.token import Token, TokenType

class Lexer:

    def __init__(self):

        self.expression_pattern = re.compile(r'^[0-9+\-*/^().,%‰|!a-zA-Z×÷π₂ʸ⁻¹²³√∛]*$')
        self.token_map = {
            '+': (TokenType.INFIX_OPERATOR, '+', '+', '+'),
            '-': (TokenType.INFIX_OPERATOR, '-', '-', '-'),
            '×': (TokenType.INFIX_OPERATOR, '×', '×', '*'),
            '÷': (TokenType.INFIX_OPERATOR, '÷', '÷', '/'),
            'div': (TokenType.INFIX_OPERATOR, ' div ', ' div ', '//'),
            'mod': (TokenType.INFIX_OPERATOR, ' mod ', ' mod ', '%'),

            '(': (TokenType.LPAREN, '(', '(', '('),
            ')': (TokenType.RPAREN, ')', ')', ')'),

            'sin': (TokenType.FUNCTION, 'sin', 'sin', 'sin'),
            'cos': (TokenType.FUNCTION, 'cos', 'cos', 'cos'),
            'tan': (TokenType.FUNCTION, 'tan', 'tan', 'tan'),
            'cot': (TokenType.FUNCTION, 'cot', 'cot', 'cot'),
            'sin⁻¹': (TokenType.FUNCTION, 'sin⁻¹', 'sin⁻¹', 'arcsin'),
            'cos⁻¹': (TokenType.FUNCTION, 'cos⁻¹', 'cos⁻¹', 'arccos'),
            'tan⁻¹': (TokenType.FUNCTION, 'tan⁻¹', 'tan⁻¹', 'arctan'),
            'cot⁻¹': (TokenType.FUNCTION, 'cot⁻¹', 'cot⁻¹', 'arccot'),

            'log': (TokenType.FUNCTION, 'log', 'log', 'log10'),
            'ln': (TokenType.FUNCTION, 'ln', 'ln', 'log'),
            '%': (TokenType.POSTFIX_OPERATOR, '%', '%', '*(1/100)'),
            'log₂': (TokenType.FUNCTION, 'log₂', 'log₂', 'log2'),
            '‰': (TokenType.POSTFIX_OPERATOR, '‰', '‰', '*(1/1000)'),

            'x²': (TokenType.INFIX_OPERATOR, 'x²', '²', '**(2)'),
            'x³': (TokenType.INFIX_OPERATOR, 'x³', '³', '**(3)'),
            'xʸ': (TokenType.INFIX_OPERATOR, 'xʸ', '^', '**'),
            'x⁻¹': (TokenType.INFIX_OPERATOR, 'x⁻¹', '⁻¹', '**(-1)'),
            '√': (TokenType.FUNCTION, '√', '√', 'sqrt'),
            '∛': (TokenType.FUNCTION, '∛', '∛', 'cbrt'),
            '×10ʸ': (TokenType.FUNCTION, '×10ʸ', '×10^', '*10**'),

            'π': (TokenType.CONSTANT, 'π', 'π', 'pi'),
            'e': (TokenType.CONSTANT, 'e', 'e', 'e'),

            'round': (TokenType.FUNCTION, 'round', 'round', 'round'),
            'floor': (TokenType.FUNCTION, 'floor', 'floor', 'floor'),
            'ceil': (TokenType.FUNCTION, 'ceil', 'ceil', 'ceil'),
            'trunc': (TokenType.FUNCTION, 'trunc', 'trunc', 'trunc'),
            'frac': (TokenType.FUNCTION, 'frac', 'frac', 'frac'),
            'sign': (TokenType.FUNCTION, 'sign', 'sign', 'sign'),
            'gamma': (TokenType.FUNCTION, 'gamma', 'gamma', 'gamma'),
            'lgamma': (TokenType.FUNCTION, 'lgamma', 'lgamma', 'lgamma'),
            'csc': (TokenType.FUNCTION, 'csc', 'csc', 'csc'),
            'sec': (TokenType.FUNCTION, 'sec', 'sec', 'sec'),
            'csc⁻¹': (TokenType.FUNCTION, 'csc⁻¹', 'csc⁻¹', 'arccsc'),
            'sec⁻¹': (TokenType.FUNCTION, 'sec⁻¹', 'sec⁻¹', 'arcsec'),
            'sinh': (TokenType.FUNCTION, 'sinh', 'sinh', 'sinh'),
            'cosh': (TokenType.FUNCTION, 'cosh', 'cosh', 'cosh'),
            'tanh': (TokenType.FUNCTION, 'tanh', 'tanh', 'tanh'),
            'csch': (TokenType.FUNCTION, 'csch', 'csch', 'csch'),
            'sech': (TokenType.FUNCTION, 'sech', 'sech', 'sech'),
            'coth': (TokenType.FUNCTION, 'coth', 'coth', 'coth'),
            'sinh⁻¹': (TokenType.FUNCTION, 'sinh⁻¹', 'sinh⁻¹', 'arcsinh'),
            'cosh⁻¹': (TokenType.FUNCTION, 'cosh⁻¹', 'cosh⁻¹', 'arccosh'),
            'tanh⁻¹': (TokenType.FUNCTION, 'tanh⁻¹', 'tanh⁻¹', 'arctanh'),
            'csch⁻¹': (TokenType.FUNCTION, 'csch⁻¹', 'csch⁻¹', 'arccsch'),
            'sech⁻¹': (TokenType.FUNCTION, 'sech⁻¹', 'sech⁻¹', 'arcsech'),
            'coth⁻¹': (TokenType.FUNCTION, 'coth⁻¹', 'coth⁻¹', 'arccoth'),

            # Need Special Handling
            '!': (TokenType.POSTFIX_OPERATOR, '!', '!', '!'),
            '|': (TokenType.FUNCTION, '|', '|', 'abs'),
            'Ans': (TokenType.NUMBER, 'Ans', 'Ans', 'Ans'),

            # For Graph Mode
            'x': (TokenType.VARIABLE, 'x', 'x', 'x'),
            '10ˣ': (TokenType.FUNCTION, '10ˣ', '10ˣ', '10**'),
            '2ˣ': (TokenType.FUNCTION, '2ˣ', '2ˣ', '2**'),
            'eˣ': (TokenType.FUNCTION, 'eˣ', 'eˣ', 'exp(x)'),
        }


    def tokenize(self, expression):

        expression = expression.replace(' ', '')

        if not self.expression_pattern.match(expression):
            raise ValueError('Error')

        tokens = []
        i = 0

        sorted_keys = sorted(self.token_map.keys(), key=len, reverse=True)

        while i < len(expression):

            matched = False
            for key in sorted_keys:
                if expression.startswith(key, i):
                    token_type, key, display_str, eval_str = self.token_map[key]
                    tokens.append(Token(token_type, key, display_str, eval_str))

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

                tokens.append(Token(TokenType.NUMBER, num, num, num))
                continue

            raise ValueError('Error')

        return tokens