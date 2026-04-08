import re

class Parser:

    def __init__(self, buttons_map):

        self.buttons_map = buttons_map
        self.sorted_tokens = sorted(buttons_map.keys(), key=len, reverse=True)
        self.expression_pattern = re.compile(r'^[0-9x+\-*/().,^ a-zA-Z]+$')


    def parse(self, expression):

        expression = expression.replace(' ', '')

        if not expression:
            return '' 

        if not self.expression_pattern.match(expression):
            raise ValueError('Error')

        display_expression = ''
        eval_expression = ''

        i = 0

        while i < len(expression):
            match = None

            for token in self.sorted_tokens:
                if expression.startswith(token, i):
                    match = token
                    break

            if match:
                display_expression += self.buttons_map[match]['append']
                eval_expression += self.buttons_map[match]['calculate']
                i += len(match)
                continue

            char = expression[i]

            if char == 'π':
                display_expression += 'π'
                eval_expression += 'pi'
                i += 1
                continue

            if char == '^':
                display_expression += '^'
                eval_expression += '**'
                i += 1
                continue

            if char.isdigit() or char == '.':
                num = char
                i += 1
                while i < len(expression) and (expression[i].isdigit() or expression[i] == '.'):
                    num += expression[i]
                    i += 1

                display_expression += num
                eval_expression += num
                continue

            if char.isalpha():
                identifier = char
                i += 1
                while i < len(expression) and expression[i].isalpha():
                    identifier += expression[i]
                    i += 1

                if identifier == 'pi':
                    display_expression += 'π'
                    eval_expression += 'pi'
                elif identifier == 'e':
                    display_expression += 'e'
                    eval_expression += 'e'
                else:
                    display_expression += identifier
                    eval_expression += identifier

                continue

            if char in '+-*/(),%':
                display_expression += char
                eval_expression += char
                i += 1
                continue

            raise ValueError('Error')

        return display_expression, eval_expression