from .expression import Expression
from ...exceptions import TypeCheckingException, TemplateEngineException
from ..general_interfaces import IGetValue, IValueHolder


class BinaryExpression(Expression):
    string_operator = None

    def __init__(self, line, lhs, rhs):
        super().__init__(line)
        self._lhs = lhs
        self._rhs = rhs

    def __repr__(self):
        return "{type}: {lhs} {operator} {rhs}".format(
            type=self.__class__.__name__,
            lhs=self._lhs,
            operator=type(self).string_operator,
            rhs=self._rhs
        )

    def __str__(self):
        return self.__repr__()

    @property
    def rhs(self):
        return self._rhs

    @property
    def lhs(self):
        return self._lhs

    def analyse(self, context=None):
        self.context = context
        self.custom_analysis()

        if self.lhs is None:
            raise TypeCheckingException("The left hand side of an expression must always be specified")
        else:
            self.lhs = self.lhs.analyse(context)

        if self.rhs is not None:
            self.rhs = self.rhs.analyse(context)

        return self

    def custom_analysis(self):
        # Override this method in order to provide additional analysis
        # for the expression
        pass

    @staticmethod
    def _extract_value_from_expression(expression):
        if isinstance(expression, IGetValue):
            return expression.get_value()
        elif isinstance(expression, IValueHolder):
            return expression.value
        raise TemplateEngineException("Left hand side of the expression has invalid type")

    def get_value(self):
        lhs_value = BinaryExpression._extract_value_from_expression(self.lhs)
        rhs_value = BinaryExpression._extract_value_from_expression(self.rhs)

        return self.get_value_operation(lhs_value, rhs_value)

    def set_value(self, value):
        # Should never be used
        # Has no effect
        pass

    def get_value_operation(self, lhs, rhs):
        raise NotImplementedError()
