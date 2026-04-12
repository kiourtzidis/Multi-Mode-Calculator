class Node:
    def evaluate(self):
        raise NotImplementedError()


class NumberNode(Node):

    def __init__(self, value):
        self.value = value


    def evaluate(self):
        return self.value


class NegNode(Node):

    def __init__(self, right):
        self.right = right


    def evaluate(self):
        return -self.right.evaluate()


class AddNode(Node):

    def __init__(self, left, right):
        self.left = left
        self.right = right


    def evaluate(self):
        return self.left.evaluate() + self.right.evaluate()


class SubNode(Node):

    def __init__(self, left, right):
        self.left = left
        self.right = right


    def evaluate(self):
        return self.left.evaluate() - self.right.evaluate()


class MulNode(Node):

    def __init__(self, left, right):
        self.left = left
        self.right = right


    def evaluate(self):
        return self.left.evaluate() * self.right.evaluate()


class DivNode(Node):

    def __init__(self, left, right):
        self.left = left
        self.right = right


    def evaluate(self):
        return self.left.evaluate() / self.right.evaluate()


class FloorDivNode(Node):

    def __init__(self, left, right):
        self.left = left
        self.right = right


    def evaluate(self):
        return self.left.evaluate() // self.right.evaluate()


class ModNode(Node):

    def __init__(self, left, right):
        self.left = left
        self.right = right


    def evaluate(self):
        return self.left.evaluate() % self.right.evaluate()