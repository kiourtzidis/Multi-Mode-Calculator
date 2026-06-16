import math
from core import math_functions
from core.token import Token, TokenType
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

            'abs': abs,
            'round': round,

            '%': lambda x: x * 0.01,
            '‰': lambda x: x * 0.001,

            '!': lambda x: math_functions.factorial(x),
            '!!': lambda x: math_functions.double_factorial(x),

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

        last = self.tokens[-1]

        if last.is_number() and len(last.key) > 1:
            trimmed = last.key[:-1]
            self.tokens[-1] = Token(TokenType.NUMBER, trimmed, trimmed, trimmed)
        else:
            self.tokens.pop()

        self._update_expressions_from_tokens()


    def append(self, symbol):

        if self.display_expression == 'Error':
            self.clear()

        if self.calculated:
            tokenized = self.lexer.tokenize(symbol)

            if tokenized and (tokenized[0].is_infix_operator() or tokenized[0].is_postfix_operator()):
                result_str = str(self.last_result)
                self.tokens = [Token(TokenType.NUMBER, result_str, result_str, result_str)]
                self.raw_input = result_str
            else:
                self.clear()

        self.calculated = False

        resolved = self._resolve_input(symbol)
        if resolved is None:
            return

        self.raw_input += resolved

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


    def _resolve_input(self, symbol):
        
        tokens = self.tokens
        last = tokens[-1] if tokens else None

        incoming_token = self.lexer.tokenize(symbol)[0]

        if not tokens and symbol == '-':
            return '-'
        
        if not tokens and incoming_token and incoming_token.is_infix_operator():
            return None

        if last and last.display_value == '+' and symbol == '-':
            self.tokens.pop()
            self._update_expressions_from_tokens()
            return '-'

        if last and last.is_infix_operator() and symbol == '-':
            return None if last.eval_value == '-' else '-'

        if symbol == '.' and (not last or not last.is_value()):
            return '0.'

        if last and last.is_infix_operator() and incoming_token and incoming_token.is_infix_operator():
            return None
        
        if incoming_token.is_function():
            return symbol + '('

        if incoming_token.is_postfix_operator() and (last and last.eval_value in ('%', '‰')):
            return None

        if last and last.display_value[-1] in ('¹', '²', '³'):
            if incoming_token and (incoming_token.is_value() or incoming_token.is_function()):
                return '×' + symbol

        return symbol


    def _update_expressions_from_tokens(self):
        self.raw_input = ''.join(token.key for token in self.tokens)
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