class Node:
    def evaluate(self):
        raise NotImplementedError()


class NumberNode(Node):

    def __init__(self, value):
        self.value = value


    def evaluate(self, scope):
        return self.value


class NegNode(Node):

    def __init__(self, right):
        self.right = right


    def evaluate(self, scope):
        return -self.right.evaluate(scope)


class AddNode(Node):

    def __init__(self, left, right):
        self.left = left
        self.right = right


    def evaluate(self, scope):
        return self.left.evaluate(scope) + self.right.evaluate(scope)


class SubNode(Node):

    def __init__(self, left, right):
        self.left = left
        self.right = right


    def evaluate(self, scope):
        return self.left.evaluate(scope) - self.right.evaluate(scope)


class MulNode(Node):

    def __init__(self, left, right):
        self.left = left
        self.right = right


    def evaluate(self, scope):
        return self.left.evaluate(scope) * self.right.evaluate(scope)


class DivNode(Node):

    def __init__(self, left, right):
        self.left = left
        self.right = right


    def evaluate(self, scope):
        return self.left.evaluate(scope) / self.right.evaluate(scope)


class FloorDivNode(Node):

    def __init__(self, left, right):
        self.left = left
        self.right = right


    def evaluate(self, scope):
        return self.left.evaluate(scope) // self.right.evaluate(scope)


class ModNode(Node):

    def __init__(self, left, right):
        self.left = left
        self.right = right


    def evaluate(self, scope):
        return self.left.evaluate(scope) % self.right.evaluate(scope)


class PowerNode(Node):

    def __init__(self, left, right):
        self.left = left
        self.right = right


    def evaluate(self, scope):
        return self.left.evaluate(scope) ** self.right.evaluate(scope)


class FunctionNode(Node):

    def __init__(self, function, arg):
        self.function = function
        self.arg = arg

    def evaluate(self, scope):
        function = scope[self.function]
        return function(self.arg.evaluate(scope))