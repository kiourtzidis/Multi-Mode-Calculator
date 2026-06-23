from core.parser import Parser
from logic.calculator_logic import CalculatorLogic

class GraphLogic(CalculatorLogic):

    def evaluate_graph(self, x):
        try:
            parser = Parser(self._expand_tokens(self.tokens))
            print(self.tokens)
            ast = parser.parse()
            print(f'ast: {ast}')
            scope = {
                  **self.function_library,
                  'x': x,
            }
            return ast.evaluate(scope)

        except Exception as e:
            print(f'Error: {e}')
            return None