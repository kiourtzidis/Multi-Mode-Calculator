import math
from . import math_functions
from .parser import Parser
from .token import Token, TokenType
from logic import token

class CalculatorLogic:

    def __init__(self):

        self.display_expression = ''
        self.eval_expression = ''
        self.parser = Parser()
        self.calculated = False
        self.last_result = None
        self.angle_mode = 'DEG'
        self.tokens = []
        self.operators = ('+', '-', '×', '÷', 'div', 'mod')
        self.eval_functions = {
            **math.__dict__,
            **math_functions.__dict__,

            'sin': lambda x: math_functions.sin(x, self.angle_mode),
            'cos': lambda x: math_functions.cos(x, self.angle_mode),
            'tan': lambda x: math_functions.tan(x, self.angle_mode),
            'sec': lambda x: math_functions.sec(x, self.angle_mode),
            'csc': lambda x: math_functions.csc(x, self.angle_mode),
            'cot': lambda x: math_functions.cot(x, self.angle_mode),

            'arcsin': lambda x: math_functions.arcsin(x, self.angle_mode),
            'arccos': lambda x: math_functions.arccos(x, self.angle_mode),
            'arctan': lambda x: math_functions.arctan(x, self.angle_mode),
            'arcsec': lambda x: math_functions.arcsec(x, self.angle_mode),
            'arccsc': lambda x: math_functions.arccsc(x, self.angle_mode),
            'arccot': lambda x: math_functions.arccot(x, self.angle_mode)
            }
        self.buttons = {
            '+': {
                'append': '+',
                'calculate': '+'
            },
            '-': {
                'append': '-',
                'calculate': '-'
            },
            '×': {
                'append': '×',
                'calculate': '*'
            },
            '÷': {
                'append': '÷',
                'calculate': '/'
            },
            'div': {
                'append': ' div ',
                'calculate': '//'
            },
            'mod': {
                'append': ' mod ',
                'calculate': '%'
            },
            '(': {
                'append': '(',
                'calculate': '('
            },
            ')': {
                'append': ')',
                'calculate': ')'
            },
            'sin': {
                'append': 'sin(',
                'calculate': 'sin('
            },
            'cos': {
                'append': 'cos(',
                'calculate': 'cos('
            },
            'tan': {
                'append': 'tan(',
                'calculate': 'tan('
            },
            'cot': {
                'append': 'cot(',
                'calculate': 'cot('
            },
            'sin⁻¹': {
                'append': 'sin⁻¹(',
                'calculate': 'arcsin('
            },
            'cos⁻¹': {
                'append': 'cos⁻¹(',
                'calculate': 'arccos('
            },
            'tan⁻¹': {
                'append': 'tan⁻¹(',
                'calculate': 'arctan('
            },
            'cot⁻¹': {
                'append': 'cot⁻¹(',
                'calculate': 'arccot('
            },
            'log': {
                'append': 'log(',
                'calculate': 'log10('
            },
            'ln': {
                'append': 'ln(',
                'calculate': 'log('
            },
            '%': {
                'append': '%',
                'calculate': '*(1/100)'
            },
            'log₂': {
                'append': 'log₂(',
                'calculate': 'log2('
            },
            '‰': {
                'append': '‰',
                'calculate': '*(1/1000)'
            },
            'x²': {
                'append': '²',
                'calculate': '**(2)'
            },
            'x³': {
                'append': '³',
                'calculate': '**(3)'
            },
            'xʸ': {
                'append': '^',
                'calculate': '**'
            },
            'x⁻¹': {
                'append': '⁻¹',
                'calculate': '**(-1)'
            },
            '10ˣ': {
                'append': '10ˣ',
                'calculate': '10**x'
            },
            '2ˣ': {
                'append': '2ˣ',
                'calculate': '2**x'
            },
            'eˣ': {
                'append': 'eˣ',
                'calculate': 'exp(x)'
            },
            '√': {
                'append': '√(',
                'calculate': 'sqrt('
            },
            '∛': {
                'append': '∛(',
                'calculate': 'cbrt('
            },
            '×10ʸ': {
                'append': '×10^',
                'calculate': '*10**'
            },
            'i': {
                'append': 'i',
                'calculate': 'j'
            },
            'π': {
                'append': 'π',
                'calculate': 'pi'
            },
            'e': {
                'append': 'e',
                'calculate': 'e'
            },
            'round': {
                'append': 'round(',
                'calculate': 'round('
            },
            'floor': {
                'append': 'floor(',
                'calculate': 'floor('
            },
            'ceil': {
                'append': 'ceil(',
                'calculate': 'ceil('
            },
            'trunc': {
                'append': 'trunc(',
                'calculate': 'trunc('
            },
            'frac': {
                'append': 'frac(',
                'calculate': 'frac('
            },
            'sign': {
                'append': 'sign(',
                'calculate': 'sign('
            },
            'gamma': {
                'append': 'gamma(',
                'calculate': 'gamma('
            },
            'lgamma': {
                'append': 'lgamma(',
                'calculate': 'lgamma('
            },
            'csc': {
                'append': 'csc(',
                'calculate': 'csc('
            },
            'sec': {
                'append': 'sec(',
                'calculate': 'sec('
            },
            'sinh': {
                'append': 'sinh(',
                'calculate': 'sinh('
            },
            'cosh': {
                'append': 'cosh(',
                'calculate': 'cosh('
            },
            'tanh': {
                'append': 'tanh(',
                'calculate': 'tanh('
            },
            'csch': {
                'append': 'csch(',
                'calculate': 'csch('
            },
            'sech': {
                'append': 'sech(',
                'calculate': 'sech('
            },
            'coth': {
                'append': 'coth(',
                'calculate': 'coth('
            },
            'csc⁻¹': {
                'append': 'csc⁻¹(',
                'calculate': 'arccsc('
            },
            'sec⁻¹': {
                'append': 'sec⁻¹(',
                'calculate': 'arcsec('
            },
            'sinh⁻¹': {
                'append': 'sinh⁻¹(',
                'calculate': 'arcsinh('
            },
            'cosh⁻¹': {
                'append': 'cosh⁻¹(',
                'calculate': 'arccosh('
            },
            'tanh⁻¹': {
                'append': 'tanh⁻¹(',
                'calculate': 'arctanh('
            },
            'csch⁻¹': {
                'append': 'csch⁻¹(',
                'calculate': 'arccsch('
            },
            'sech⁻¹': {
                'append': 'sech⁻¹(',
                'calculate': 'arcsech('
            },
            'coth⁻¹': {
                'append': 'coth⁻¹(',
                'calculate': 'arccoth('
            }
        }


    def clear(self):
        self.tokens.clear()
        self.display_expression = ''
        self.eval_expression = ''
        self.calculated = False


    def backspace(self):

        if not self.tokens:
            return

        self.tokens.pop()
        self._update_expressions_from_tokens()


    def append(self, symbol):

        if self.display_expression == 'Error':
            self.clear()

        if self.calculated:
            if symbol.isdigit() or symbol in (
                '.', 'sin', 'cos', 'tan', 'sec', 'csc', 'cot', 'sin⁻¹', 'cos⁻¹', 'tan⁻¹', 'cot⁻¹',
                'sinh', 'cosh', 'tanh', 'sech', 'csch', 'coth', 'sec⁻¹', 'csc⁻¹', 'sinh⁻¹', 'cosh⁻¹', 
                'tanh⁻¹', 'sech⁻¹', 'csc⁻¹', 'coth⁻¹', 'round', 'floor', 'ceil', 'trunc', 'frac', 
                'sign', 'gamma', 'lgamma', 'log', 'ln', '|x|', 'log₂', '√', '∛', 'e', 'π', 'Ans'
                ):             
                self.clear()

        self.calculated = False

        try:
            new_tokens = self.parser.tokenize(symbol)

        except ValueError:
            self.display_expression = 'Error'
            self.eval_expression = ''
            return

        first = new_tokens[0]
        last = self.tokens[-1] if self.tokens else None

        if first.type == TokenType.OPERATOR:

            if not self.tokens and first.display_value == '-':
                self.tokens.append(Token(TokenType.OPERATOR, '-', '-'))
                self._update_expressions_from_tokens()
                return

            if not self.tokens:
                return

            if last and last.type == TokenType.OPERATOR:
                if first.display_value == '-' and last.display_value != '-':
                    self.tokens.append(Token(TokenType.OPERATOR, '-', '-'))
                    self._update_expressions_from_tokens()
                return

        if first.type == TokenType.NUMBER or first.display_value in ('%', '‰'):
            if last and last.display_value in ('%', '‰'):
                return

        if first.display_value == '.': 
            if not last or last.type != TokenType.NUMBER:    
                self.tokens.append(Token(TokenType.NUMBER, '0', '0'))
                self._update_expressions_from_tokens()

        if self.tokens:
            last = self.tokens[-1]

            if (
            first.display_value not in (
            '+', '-', '÷', 'div', 'mod', '(', ')', '!', 'x²', 'x³', 'xʸ', 'x⁻¹',
            'sin', 'cos', 'tan', 'sec', 'csc', 'cot', 'sin⁻¹', 'cos⁻¹', 'tan⁻¹', 'cot⁻¹',
            'sinh', 'cosh', 'tanh', 'sech', 'csch', 'coth', 'sinh⁻¹', 'cosh⁻¹', 'tanh⁻¹', 
            'sech⁻¹', 'csc⁻¹', 'coth⁻¹', 'round', 'floor', 'ceil', 'trunc', 'frac', 'sign', 
            'gamma', 'lgamma', 'log', 'log₂', 'ln')
            and last.display_value[-1] in ('¹', '²', '³')
            ):      
                self.tokens.append(Token(TokenType.OPERATOR, '×', '*'))
                self._update_expressions_from_tokens()
                
            elif first.display_value in ('x⁻¹', 'x²', 'x³') and last.display_value in ('¹', '²', '³'):
                self.tokens.append(Token(TokenType.OPERATOR, '^', '**'))
                self._update_expressions_from_tokens()

            
            if last and last.display_value == 'Ans':
                if first.type == TokenType.NUMBER or first.display_value in (
                'sin', 'cos', 'tan', 'sec', 'csc', 'cot', 'sin⁻¹', 'cos⁻¹', 'tan⁻¹', 'cot⁻¹',
                'sinh', 'cosh', 'tanh', 'sech', 'csch', 'coth', 'sinh⁻¹', 'cosh⁻¹', 'tanh⁻¹', 
                'sech⁻¹', 'csc⁻¹', 'coth⁻¹', 'round', 'floor', 'ceil', 'trunc', 'frac', 'sign',
                'gamma', 'lgamma', 'log', 'log₂', 'ln', 'π', 'e'
                ):
                    self.tokens.append(Token(TokenType.OPERATOR, '×', '*'))
                    self._update_expressions_from_tokens()

        if symbol == 'a×b':

            number = ''

            for char in self.eval_expression[::-1]:
                if char.isdigit() or char == '.':
                    number = char + number
                else:
                    break

            if number:
                if '.' in number:
                    number = float(number)
                else:
                    number = int(number)
            else:
                return

            factorized = math_functions.factorize(number)

            if not factorized:
                return

            number = str(number)

            self.tokens = self.tokens[:-len(number)]
            for char in factorized:
                self.tokens.append(Token(TokenType.NUMBER, char, char))

            self._update_expressions_from_tokens()
            return

        if symbol == 'Ans':
            if self.last_result:
                if self.tokens and last and last.type not in (TokenType.OPERATOR, TokenType.PARENTHESIS):
                    self.tokens.append(Token(TokenType.OPERATOR, '×', '*'))

                self.tokens.append(Token(TokenType.NUMBER, 'Ans', self.last_result))
                self._update_expressions_from_tokens()

            return

        for token in new_tokens:
            self.tokens.append(token)

        self._update_expressions_from_tokens()


    def calculate(self):

        try:

            original_expression = self.display_expression

            check_expression = self.eval_expression.lstrip('-')

            contains_operation = (
                check_expression in ('pi', 'e') 
                or any(operator in check_expression for operator in (
                    '+', '-', '*', '/', '//', '%', '**', '('
                )))

            if not contains_operation:
                return None, None

            self.eval_expression = self._add_implicit_multiplication(self.eval_expression)

            result = eval(self.eval_expression, self.eval_functions)
            result = self._clean_result(result)

            if isinstance(result, float) and result.is_integer():
                result = int(result)

            self.display_expression = f'{result:.10g}'
            self.eval_expression = f'{result:.10g}'
            self.last_result = self.eval_expression

            for char in str(result):
                self.tokens.append((char, char))

            self.calculated = True

            return original_expression, self.eval_expression

        except Exception:

            self.tokens.clear()
            self.display_expression = 'Error'
            self.eval_expression = ''
            self.calculated = False 
            return None, 'Error'


    def toggle_angle_mode(self):
        self.angle_mode = 'RAD' if self.angle_mode == 'DEG' else 'DEG'


    def _add_implicit_multiplication(self, expression):

        processed_expression = ''

        for i in range(len(expression)):

            current_char = expression[i]
            processed_expression += current_char

            if i < len(expression) - 1:

                next_char = expression[i+1]

                if current_char.isdigit() and next_char.isdigit():
                    continue

                left_value = (
                    current_char.isdigit() 
                    or current_char == ')'
                )

                right_value = (
                    next_char.isdigit()
                    or next_char.isalpha() 
                    or next_char == '('
                )

                if left_value and right_value:
                    processed_expression += '*'

        if 'log10*' in processed_expression:
            processed_expression = processed_expression.replace('log10*', 'log10')
        if 'log2*' in processed_expression:
            processed_expression = processed_expression.replace('log2*', 'log2')

        return processed_expression
    

    def _update_expressions_from_tokens(self):
        self.display_expression = ''.join(token.display_value for token in self.tokens)
        self.eval_expression = ''.join(token.eval_value for token in self.tokens)


    def _clean_result(self, result):
        if isinstance(result, float):
            if abs(result) < 1e-10:
                return 0
            if abs(result - round(result)) < 1e-10:
                return int(round(result))
            return round(result, 12)
        return result