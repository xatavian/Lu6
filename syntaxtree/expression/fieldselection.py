from .expression import Expression
from ..variable import Variable
from exceptions import TemplateEngineException


class FieldSelection(Expression):

    def __init__(self, line, identifier):
        super().__init__(line)
        self._target = Variable(identifier.line, identifier.identifiers[:-2])
        self._field = identifier.identifiers[-1]

    def analyse(self, context=None):
        self._target.analyse(self.context)

    def get_value(self):
        target_value = self._target.get_value()
        return getattr(target_value, self._field)

    def set_value(self, value):
        target_value = self._target.get_value()
        setattr(target_value, self._field, value)
