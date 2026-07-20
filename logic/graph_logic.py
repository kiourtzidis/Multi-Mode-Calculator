from logic.calculator_logic import CalculatorLogic
from core.parser import Parser
from core.exceptions import MathError

class GraphLogic(CalculatorLogic):

    def evaluate_graph(self, x):
        try:
            parser = Parser(self._expand_tokens(self.tokens))

            ast = parser.parse()
            scope = {
                  **self.function_library,
                  'x': x
            }
            return ast.evaluate(scope)

        except MathError:
            return None