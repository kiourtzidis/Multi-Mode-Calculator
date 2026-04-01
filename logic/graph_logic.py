import numpy as np
from logic.calculator_logic import CalculatorLogic

class GraphLogic(CalculatorLogic):

        def __init__(self):
            
            super().__init__()
            
            self.numpy_functions = {
            'sin': np.sin,
            'cos': np.cos,
            'tan': np.tan,
            'sec': lambda x: 1/np.cos(x),
            'csc': lambda x: 1/np.sin(x),
            'cot': lambda x: 1/np.tan(x),
            'arcsin': np.arcsin,
            'arccos': np.arccos,
            'arctan': np.arctan,
            'arcsec': lambda x: np.arccos(1/x),
            'arccsc': lambda x: np.arcsin(1/x),
            'arccot': lambda x: np.arctan(1/x),
            'x²': lambda x: x**2,
            'x³': lambda x: x**3,
            'log': np.log10,
            'log₂': np.log2,
            'ln': np.log,
            'sqrt': np.sqrt,
            'cbrt': np.cbrt,
            'abs': np.abs,
            'exp': np.exp,
            'pi': np.pi,
            'e': np.e
        }
            
        def evaluate_graph(self, x):

             try:
                return eval(self.eval_expression, {'__builtins__': {}}, {**self.numpy_functions, 'x': x})
             
             except:
                return None