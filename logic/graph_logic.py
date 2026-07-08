from logic.calculator_logic import CalculatorLogic
from core.parser import Parser
from core.exceptions import MathError

class GraphLogic(CalculatorLogic):

    def evaluate_graph(self, x):
        try:
            parser = Parser(self._expand_tokens(self.tokens))
            print(self.tokens)

            ast = parser.parse()
            scope = {
                  **self.function_library,
                  'x': x
            }
            return ast.evaluate(scope)

        except MathError as e:
            print(f'Error: {e}')
            return None