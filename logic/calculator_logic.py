import math
from core import math_functions
from core.lexer import Lexer
from core.parser import Parser

class CalculatorLogic:

    def __init__(self):

        self.raw_input = ''
        self.display_expression = ''
        self.eval_expression = ''
        self.calculated = False
        self.last_result = None
        self.angle_mode = 'DEG'
        self.tokens = []
        self.lexer = Lexer()
        self.function_library = {
            **math.__dict__,
            **math_functions.__dict__,

            '%': lambda x: x * 0.01,
            '‰': lambda x: x * 0.001,
            '!': lambda x: math_functions.factorial(x),

            'sin': lambda x: math_functions.sin(x, self.angle_mode),
            'cos': lambda x: math_functions.cos(x, self.angle_mode),
            'tan': lambda x: math_functions.tan(x, self.angle_mode),
            'csc': lambda x: math_functions.csc(x, self.angle_mode),
            'sec': lambda x: math_functions.sec(x, self.angle_mode),
            'cot': lambda x: math_functions.cot(x, self.angle_mode),

            'arcsin': lambda x: math_functions.arcsin(x, self.angle_mode),
            'arccos': lambda x: math_functions.arccos(x, self.angle_mode),
            'arctan': lambda x: math_functions.arctan(x, self.angle_mode),
            'arccsc': lambda x: math_functions.arccsc(x, self.angle_mode),
            'arcsec': lambda x: math_functions.arcsec(x, self.angle_mode),
            'arccot': lambda x: math_functions.arccot(x, self.angle_mode)
            }


    def clear(self):
        self.tokens.clear()
        self.raw_input = ''
        self.display_expression = ''
        self.eval_expression = ''
        self.calculated = False


    def backspace(self):

        if not self.tokens:
            return

        deleted_token = self.tokens.pop()

        if deleted_token.is_value():
            self.raw_input = self.raw_input[:-1]
        else:
            self.raw_input = self.raw_input[:-len(deleted_token.key)]

        self.tokens = self.lexer.tokenize(self.raw_input)
        self._update_expressions_from_tokens()


    def append(self, symbol):

        if self.display_expression == 'Error':
            self.clear()

        if self.calculated:
            self.clear()

        self.calculated = False

        self.raw_input += symbol

        try:
            self.tokens = self.lexer.tokenize(self.raw_input)
            print(self.tokens)
            self._update_expressions_from_tokens()

        except ValueError as v:
            print(f'{v}')
            self.raw_input = ''
            self.display_expression = 'Error'
            self.eval_expression = ''
            self.tokens.clear()


    def calculate(self):

        try:
            if not self.tokens:
                return

            original_expression = self.display_expression

            parser = Parser(self.tokens)
            print(f'tokens: {self.tokens}')
            ast = parser.parse()
            print(f'ast: {ast}')
            scope = {
                **self.function_library,
                'Ans': self.last_result
            }
            result = ast.evaluate(scope)
            result = self._clean_result(result)

            self.raw_input = ''
            self.display_expression = f'{result:.10g}'
            self.eval_expression = f'{result:.10g}'
            self.last_result = result

            self.calculated = True

            return original_expression, result

        except Exception as e:
            print(f'Error: {e}')
            self.tokens.clear()
            self.raw_input = ''
            self.display_expression = 'Error'
            self.eval_expression = ''
            self.calculated = False 
            return None, 'Error'


    def toggle_angle_mode(self):
        self.angle_mode = 'RAD' if self.angle_mode == 'DEG' else 'DEG'


    def _update_expressions_from_tokens(self):
        self.display_expression = ''.join(token.display_value for token in self.tokens)
        self.eval_expression = ''.join(token.eval_value for token in self.tokens)


    def _clean_result(self, result):
        if isinstance(result, float):
            if abs(result) < 1e-10:
                return 0
            if abs(result - round(result)) < 1e-10:
                return int(round(result))
            if result.is_integer():
                return int(result)
            return round(result, 12)
        return result