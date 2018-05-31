from ...exceptions import TypeCheckingException

from .arithmeticexpressions import MultiplicationExpression, AdditionExpression,\
                                    DivisionExpression, RemainderExpression, \
                                    SubtractionExpression
from .binaryexpression import BinaryExpression
from ..general_interfaces import IGetValue, IValueHolder
from ..variable import Variable


class AssignementExpression(BinaryExpression):
    string_operator = "="

    def custom_analysis(self):
        if not isinstance(self.lhs, Variable):
            raise TypeCheckingException("The left hand side of an assignment expression can only be a variable",
                                        self.line)

        self.lhs.analyse_as_lhs(self.context)

    def get_value(self):
        if isinstance(self.rhs, IGetValue):
            self.lhs.set_value( self.get_value_operation(self.lhs.get_value(), self.rhs.get_value()))
        elif isinstance(self.rhs, IValueHolder):
            self.lhs.set_value(self.get_value_operation(self.lhs.get_value(), self.rhs.value))

        return self.lhs.get_value()

    def get_value_operation(self, lhs_value, rhs_value):
        # Override this method to provide custom assignment operation
        return rhs_value


class AssignmentMultiplicationExpression(MultiplicationExpression, AssignementExpression):
    string_operator = "*="

    def custom_analysis(self):
        # For a arithmetic assignment, the lhs must have been previously defined
        if not isinstance(self.lhs, Variable):
            raise TypeCheckingException("The left hand side of an assignment expression can only be a variable",
                                        self.line)

        self.lhs.analyse(self.context)


class AssignmentAdditionExpression(AdditionExpression, AssignementExpression):
    string_operator = "+="

    def custom_analysis(self):
        # For a arithmetic assignment, the lhs must have been previously defined
        if not isinstance(self.lhs, Variable):
            raise TypeCheckingException("The left hand side of an assignment expression can only be a variable",
                                        self.line)

        self.lhs.analyse(self.context)


class AssignmentSubtractionExpression(SubtractionExpression, AssignementExpression):
    string_operator = "-="

    def custom_analysis(self):
        # For a arithmetic assignment, the lhs must have been previously defined
        if not isinstance(self.lhs, Variable):
            raise TypeCheckingException("The left hand side of an assignment expression can only be a variable",
                                        self.line)

        self.lhs.analyse(self.context)


class AssignmentDivisionExpression(DivisionExpression, AssignementExpression):
    string_operator = "/="

    def custom_analysis(self):
        # For a arithmetic assignment, the lhs must have been previously defined
        if not isinstance(self.lhs, Variable):
            raise TypeCheckingException("The left hand side of an assignment expression can only be a variable",
                                        self.line)

        self.lhs.analyse(self.context)


class AssignmentRemainderExpression(RemainderExpression, AssignementExpression):
    string_operator = "%="

    def custom_analysis(self):
        # For a arithmetic assignment, the lhs must have been previously defined
        if not isinstance(self.lhs, Variable):
            raise TypeCheckingException("The left hand side of an assignment expression can only be a variable",
                                        self.line)

        self.lhs.analyse(self.context)
