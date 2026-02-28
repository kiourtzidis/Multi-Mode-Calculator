class CalculatorLogic:

    def __init__(self):

        self.expression = ''
        self.calculated = False
        self.history = []
        self.operators = ('+', '-', '×', '÷', 'mod', 'div')
        self.angle_mode = 'DEG'

    
    def clear(self):
        self.expression = ''
        self.calculated = False

    

    def backspace(self):
        self.expression = self.expression[:-1]
        self.calculated = False



    def append(self, symbol):

        if self.expression == 'Error':
            self.expression = ''

        if self.calculated:
            if symbol.isdigit() or symbol == '.':
                self.expression = ''

        self.calculated = False

        ends_with_operator = any(self.expression.endswith(op) for op in self.operators)

        if symbol in self.operators:

            if self.expression == '' and symbol == '-':
                self.expression = '-'
                return
            
            if self.expression == '':
                return
            
            if ends_with_operator:
                
                if symbol == '-' and not self.expression.endswith('-'):
                    self.expression += '-' 
                    return
                
                return

        if symbol == '.' and (self.expression == '' or not self.expression[-1].isdigit()):
            self.expression += '0'

        self.expression += symbol
    

    def calculate(self):

        try:
            
            if not any(op in self.expression for op in self.operators):
                return None, self.expression

            original_expression = self.expression

            expression = self.expression.replace(' ', '')
            expression = expression.replace('×', '*').replace('÷', '/')
            expression = expression.replace('mod', '%').replace('div', '//')

            result = eval(expression)

            if isinstance(result, float) and result.is_integer():
                result = int(result)

            self.history.append(f'{expression} = {result}')
            
            self.expression = str(result)
            self.calculated = True

            return original_expression, self.expression

        except Exception:

            self.expression = 'Error'
            self.calculated = False 
            return None, 'Error'
        

    def clear_history(self):
        self.history.clear()

    
    def toggle_angle_mode(self):
        self.angle_mode = 'RAD' if self.angle_mode == 'DEG' else 'DEG'