from syntaxtree.expression.binaryexpression import BinaryExpression


class ArithmeticExpression(BinaryExpression):
    string_operator = None

    def get_value_operation(self, lhs, rhs):
        raise NotImplementedError()


class AdditionExpression(ArithmeticExpression):
    string_operator = "+"

    def get_value_operation(self, lhs, rhs):
        return lhs + rhs


class MultiplicationExpression(ArithmeticExpression):
    string_operator = "*"

    def get_value_operation(self, lhs, rhs):
        return lhs * rhs


class DivisionExpression(ArithmeticExpression):
    string_operator = "/"

    def get_value_operation(self, lhs, rhs):
        return lhs / rhs


class SubtractionExpression(ArithmeticExpression):
    string_operator = "-"

    def get_value_operation(self, lhs, rhs):
        return lhs - rhs


class RemainderExpression(ArithmeticExpression):
    string_operator = "%"

    def get_value_operation(self, lhs, rhs):
        return lhs % rhs


class AndExpression(ArithmeticExpression):
    string_operator = "&&"

    def get_value_operation(self, lhs, rhs):
        return lhs and rhs


class OrExpression(ArithmeticExpression):
    string_operator = "||"

    def get_value_operation(self, lhs, rhs):
        return lhs or rhs


class EqualsExpression(ArithmeticExpression):
    string_operator = "=="

    def get_value_operation(self, lhs, rhs):
        return lhs == rhs


class GreaterExpression(ArithmeticExpression):
    string_operator = ">="

    def get_value_operation(self, lhs, rhs):
        return lhs >= rhs


class StrictGreaterExpression(ArithmeticExpression):
    string_operator = ">"

    def get_value_operation(self, lhs, rhs):
        return lhs > rhs


class SmallerExpression(ArithmeticExpression):
    string_operator = "<="

    def get_value_operation(self, lhs, rhs):
        return lhs <= rhs


class StrictSmallerExpression(ArithmeticExpression):
    string_operator = "<"

    def get_value_operation(self, lhs, rhs):
        return lhs < rhs
