import math
from . import math_functions
from .parser import Parser
from .token import Token, TokenType

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

        self.display_expression += symbol

        try:
            self.display_expression, eval_expression = self.parser.parse(symbol)
            new_tokens = self.parser.tokenize(symbol)

        except ValueError:
            self.display_expression = 'Error'
            self.eval_expression = ''
            return

        first = new_tokens[0]
        last = self.tokens[-1] if self.tokens else None

        if first.is_operator():

            if not self.tokens and first.display_value == '-':
                self.tokens.append(Token(TokenType.OPERATOR, '-', '-'))
                self._update_expressions_from_tokens()
                return

            if not self.tokens:
                return

            if last and last.is_operator():
                if first.display_value == '-' and last.display_value != '-':
                    self.tokens.append(Token(TokenType.OPERATOR, '-', '-'))
                    self._update_expressions_from_tokens()
                return

        if first.is_value() or first.display_value in ('%', '‰'):
            if last and last.display_value in ('%', '‰'):
                return

        if first.display_value == '.': 
            if not last or not last.is_value():
                self.tokens.append(Token(TokenType.NUMBER, '0', '0'))
                self._update_expressions_from_tokens()

        if self.tokens:
            last = self.tokens[-1]

            if (not first.is_operator() and not first.is_function() and not first.is_parenthesis()
            and last.display_value[-1] in ('¹', '²', '³')
            ):      
                self.tokens.append(Token(TokenType.OPERATOR, '×', '*'))
                self._update_expressions_from_tokens()
                
            elif first.display_value in ('x⁻¹', 'x²', 'x³') and last.display_value in ('¹', '²', '³'):
                self.tokens.append(Token(TokenType.OPERATOR, '^', '**'))
                self._update_expressions_from_tokens()

            
            if last and last.display_value == 'Ans':
                if first.is_value() or first.is_function():
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
                if self.tokens and last and not last.is_operator() and not last.is_parenthesis():
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