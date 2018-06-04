from .expression import Expression
from ...exceptions import TemplateEngineException
from ..variable import Variable

class MessageExpression(Expression):

    def __init__(self, line, expression, call_params):
        super().__init__(line)
        self._function = None
        if expression.is_field_selection: # Expression with form $a.b($c, $d, ...)
            self._function = FieldSelection(line, expression)
        else:
            self._function = Variable.from_qualified_identifier(expression)

        self._params = call_params

    def get_value(self):
        func = self._function.get_value()
        if not callable(func):
            raise TemplateEngineException("{function} is not a function".format(function=func), self.line)

        values = []
        for param in self._params:
            values.append(param.get_value()) #  Guarenteed by the fact that parameters are expressions
        return func(*values)

    def set_value(self, value):
        pass

    def analyse(self, context=None):
        self.context = context
        self._function.analyse(self.context)

        # TODO: check that self._params has the same number of params that
        #       self._function requires
        for param in self._params:
            param.analyse(self.context)
