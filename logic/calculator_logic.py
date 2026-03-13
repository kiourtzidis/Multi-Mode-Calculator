import math

class CalculatorLogic:

    def __init__(self):

        self.display_expression = ''
        self.eval_expression = ''
        self.calculated = False
        self.angle_mode = 'DEG'
        self.operators = ('+', '-', '×', '÷', 'mod', 'div')
        self.eval_functions = {
            **math.__dict__,
            'cbrt': self.cbrt,
            'sin': self.sin,
            'cos': self.cos,
            'tan': self.tan,
            'arcsin': self.arcsin,
            'arccos': self.arccos,
            'arctan': self.arctan
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
                'append': '',
                'calculate': '' # Will add later
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
                'calculate': 'abs('
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
                'calculate': '**2'
            },
            'x³': {
                'append': '³',
                'calculate': '**3'
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
        self.display_expression = ''
        self.eval_expression = ''
        self.calculated = False


    def backspace(self):
        self.display_expression = self.display_expression[:-1]
        self.eval_expression = self.eval_expression[:-1]
        self.calculated = False


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
            self.display_expression += '0'
            self.eval_expression += '0'

        if symbol == '|x|':

            count = self.display_expression.count('|')

            self.display_expression += '|'

            if count % 2 == 0:
                if self.eval_expression[-1].isdigit() or self.eval_expression[-1] in (')', 'i', 'e'):
                    self.eval_expression += '*abs('
                else:
                    self.eval_expression += 'abs('
            else:
                self.eval_expression += ')'
            
            return
        
        try:

            prev_char = self.eval_expression[-1]

            if self.eval_expression and not (prev_char.isdigit() and eval_symbol[0].isdigit()):

                left_value = (
                    prev_char.isdigit()
                    or prev_char in (')', 'i', 'e')
                )

                right_value = (
                    eval_symbol[0].isdigit()
                    or eval_symbol.startswith(('(', 'sin', 'cos', 'tan', 'arcsin', 'arccos', 'arctan', 'log', 'log2', 'log10', 'sqrt', 'cbrt', 'abs', 'exp', 'pi', 'e'))
                )

                if left_value and right_value:
                    self.eval_expression += '*'

        except IndexError:
            pass
            
                
        self.display_expression += display_symbol
        self.eval_expression += eval_symbol
    

    def calculate(self):

        try:

            original_expression = self.display_expression
            
            if self.eval_expression in ('pi', 'e'):
                contains_operation = True
            else:
                contains_operation = any(operator in self.eval_expression for operator in (
                    '+', '-', '*', '/', '%', '//', '**', '('
                ))

            if not contains_operation:
                return None, None

            result = eval(self.eval_expression, self.eval_functions)

            if isinstance(result, float) and result.is_integer():
                result = int(result)
            
            self.display_expression = f'{result:.10g}'
            self.eval_expression = f'{result:.10g}'

            self.calculated = True

            return original_expression, self.eval_expression

        except Exception:

            self.display_expression = 'Error'
            self.eval_expression = ''
            self.calculated = False 
            return None, 'Error'

    
    def toggle_angle_mode(self):
        self.angle_mode = 'RAD' if self.angle_mode == 'DEG' else 'DEG'

    
    def cbrt(self, x):
        return x ** (1/3)
    

    def sin(self, x):
        if self.angle_mode == 'DEG':
            x = math.radians(x)
        return round(math.sin(x), 12)


    def cos(self, x):
        if self.angle_mode == 'DEG':
            x = math.radians(x)
        return round(math.cos(x), 12)
    

    def tan(self, x):
        if self.angle_mode == 'DEG':
            x = math.radians(x)
        return round(math.tan(x), 12)
    

    def arcsin(self, x):
        result = math.asin(x)
        if self.angle_mode == 'DEG':
            result = math.degrees(result)
        return round(result, 12)    


    def arccos(self, x):
        result = math.acos(x)
        if self.angle_mode == 'DEG':
            result = math.degrees(result)
        return round(result, 12)    


    def arctan(self, x):
        result = math.atan(x)
        if self.angle_mode == 'DEG':
            result = math.degrees(result)
        return round(result, 12)