import math
from . import math_functions

class CalculatorLogic:

    def __init__(self):

        self.display_expression = ''
        self.eval_expression = ''
        self.calculated = False
        self.angle_mode = 'DEG'
        self.tokens = []
        self.operators = ('+', '-', '×', '÷', 'div', 'mod')
        self.eval_functions = {
            **math.__dict__,
            **math_functions.__dict__,

            'sin': lambda x: math_functions.sin(x, self.angle_mode),
            'cos': lambda x: math_functions.cos(x, self.angle_mode),
            'tan': lambda x: math_functions.tan(x, self.angle_mode),
            'arcsin': lambda x: math_functions.arcsin(x, self.angle_mode),
            'arccos': lambda x: math_functions.arccos(x, self.angle_mode),
            'arctan': lambda x: math_functions.arctan(x, self.angle_mode)
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
            '!': {
                'append': '!',
                'calculate': ''
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
            'arcsin': {
                'append': 'arcsin(',
                'calculate': 'arcsin('
            },
            'arccos': {
                'append': 'arccos(',
                'calculate': 'arccos('
            },
            'arctan': {
                'append': 'arctan(',
                'calculate': 'arctan('
            },
            'log': {
                'append': 'log(',
                'calculate': 'log10('
            },
            'ln': {
                'append': 'ln(',
                'calculate': 'log('
            },
            '|x|': {
                'append': '|', 
                'calculate': ''
            },
            'log₂': {
                'append': 'log₂(',
                'calculate': 'log2('
            },
            'eˣ': {
                'append': 'e^(',
                'calculate': 'exp('
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
            '√': {
                'append': '√(',
                'calculate': 'sqrt('
            },
            '∛': {
                'append': '∛(',
                'calculate': 'cbrt('
            },
            'ʸ√': {
                'append': '',
                'calculate': '' # Will add later
            },
            'π': {
                'append': 'π',
                'calculate': 'pi'
            },
            'e': {
                'append': 'e',
                'calculate': 'e'
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
        
        display_token, eval_token = self.tokens.pop()

        self.display_expression = self.display_expression[:-len(display_token)]
        self.eval_expression = self.eval_expression[:-len(eval_token)]


    def append(self, symbol):

        if self.display_expression == 'Error':
            self.display_expression = ''
            self.eval_expression = ''

        if self.calculated:
            if symbol.isdigit() or symbol in (
                '.', 'sin', 'cos', 'tan', 'arcsin', 'arccos', 'arctan', 
                'log', 'ln', '|x|', 'log₂', 'eˣ', '√', '∛', 'ʸ√', 'e', 'π'
                ):             
                self.display_expression = ''
                self.eval_expression = ''

        self.calculated = False

        if symbol in self.buttons:
            display_symbol = self.buttons[symbol]['append']
            eval_symbol = self.buttons[symbol]['calculate']

        else:
            display_symbol = symbol
            eval_symbol = symbol

        ends_with_operator = any(self.display_expression.endswith(operator) for operator in self.operators)

        if symbol in self.operators:

            if self.display_expression == '' and symbol == '-':
                self.display_expression = '-'
                self.eval_expression = '-'
                return
            
            if self.display_expression == '':
                return
            
            if ends_with_operator:
                if symbol == '-' and not self.display_expression.endswith('-'):
                    self.display_expression += '-'
                    self.eval_expression += '-'
                    return              
                return

        if symbol == '.' and (self.display_expression == '' or not self.display_expression[-1].isdigit()):
            self.tokens.append(('0', '0'))
            self.display_expression += '0'
            self.eval_expression += '0'

        try:

            if symbol not in self.operators and self.display_expression[-1] in ('²', '³'):
                self.tokens.append(('×', '*'))
                self.display_expression += '×'

        except IndexError:
            pass

        if symbol == '!':

            if not self.eval_expression:
                return

            i = len(self.eval_expression) - 1
            operand = ''

            if self.eval_expression[i].isdigit():
                while i >= 0 and self.eval_expression[i].isdigit():
                    operand = self.eval_expression[i] + operand
                    i -= 1

            elif self.eval_expression[i] == ')':
                bracket_count = 0

                while i >= 0:
                    char = self.eval_expression[i]
                    operand = char + operand

                    if char == ')':
                        bracket_count += 1
                    elif char == '(':
                        bracket_count -= 1

                    i -= 1

                    if bracket_count == 0:
                        break

                while i >= 0 and self.eval_expression[i].isalpha():
                    operand = self.eval_expression[i] + operand
                    i -= 1

            else:
                return

            self.eval_expression = self.eval_expression[:-len(operand)-1]
            self.eval_expression += f'factorial({operand})'

            self.display_expression += '!'

            self.tokens.append(('!', 'factorial('))
            self.tokens.append((')', ')'))

            return


        if symbol == '|x|':

            count = self.display_expression.count('|')

            self.display_expression += '|'

            if count % 2 == 0:
                self.eval_expression += 'abs('
                self.tokens.append(('|', 'abs('))
            else:
                self.eval_expression += ')'
                self.tokens.append(('|', ')'))
            
            return
        
        self.tokens.append((display_symbol, eval_symbol))
            
        self.display_expression += display_symbol
        self.eval_expression += eval_symbol 
    

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
            print(f'{self.tokens}\ndisplay: ', self.display_expression)
            try:
                print('eval: ', self.eval_expression)
            except Exception as e:
                print('eval failed:', e)
            result = eval(self.eval_expression, self.eval_functions)

            if isinstance(result, float) and result.is_integer():
                result = int(result)
            
            self.display_expression = f'{result:.10g}'
            self.eval_expression = f'{result:.10g}'

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