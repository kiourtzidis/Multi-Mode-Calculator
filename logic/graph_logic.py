import re
import sympy as sp
from sympy import symbols, lambdify, parse_expr
from logic.calculator_logic import CalculatorLogic

class GraphLogic(CalculatorLogic):

        def __init__(self):
            
            super().__init__()
            
            self.sympy_functions = {
               'x': symbols('x'),

               'sin': sp.sin,
               'cos': sp.cos,
               'tan': sp.tan,

               'sec': lambda x: 1/sp.cos(x),
               'csc': lambda x: 1/sp.sin(x),
               'cot': lambda x: 1/sp.tan(x),

               'arcsin': sp.asin,
               'arccos': sp.acos,
               'arctan': sp.atan,

               'arcsec': lambda x: sp.acos(1/x),
               'arccsc': lambda x: sp.asin(1/x),
               'arccot': lambda x: sp.atan(1/x),

               'sqrt': sp.sqrt,
               'abs': sp.Abs,
               'exp': sp.exp,

               'log': sp.log,
               'log10': lambda x: sp.log(x, 10),
               'log2': lambda x: sp.log(x, 2),

               'pi': sp.pi,
               'e': sp.E
        }

            self.expression_pattern = re.compile(r'^[0-9x+\-*/().,^ a-zA-Z]+$')


        def evaluate_graph(self, x):

            try:
               x_symbol = self.sympy_functions['x']

               self.eval_expression = self.eval_expression.replace('^', '**')
               self.eval_expression = self._add_implicit_multiplication(self.eval_expression)

               if not self.expression_pattern.match(self.eval_expression.replace(' ', '')):
                  raise ValueError('Error')

               graph_expression = parse_expr(
                self.eval_expression,
                local_dict=self.sympy_functions,
                global_dict={
                    'Integer': sp.Integer,
                    'Float': sp.Float
                }
            )

               f = lambdify(x_symbol, graph_expression, 'numpy')

               y = f(x)

               return y

            except Exception as e:
               print(f"Error evaluating graph expression: {e}")
               return None