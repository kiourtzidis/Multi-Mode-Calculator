import sympy as sp
from sympy import symbols, sympify, lambdify
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

               'log': sp.log,
               'log10': lambda x: sp.log(x, 10),
               'log2': lambda x: sp.log(x, 2),

               'sqrt': sp.sqrt,
               'abs': sp.Abs,
               'exp': sp.exp,

               'pi': sp.pi,
               'e': sp.E
        }
            
        def evaluate_graph(self, x):

            try:
               print("EXPR:", self.eval_expression)
               x_symbol = self.sympy_functions['x']

               graph_expression = sympify(self.eval_expression, locals=self.sympy_functions)
               print("SYMPY EXPR:", graph_expression)
               f = lambdify(x_symbol, graph_expression, 'numpy')

               y = f(x)

               return y

            except Exception as e:
               print("Error evaluating graph:", e)
               return None