from logic.parser import Parser
from logic.calculator_logic import CalculatorLogic

class GraphLogic(CalculatorLogic):

        def evaluate_graph(self, x):
         try:
            parser = Parser(self.tokens)
            ast = parser.parse()
            scope = {
                  'x': x,
                  **self.function_library
            }
            return ast.evaluate(scope)

         except Exception as e:
            print(f'Error: {e}')
            return None