from .expression import Expression
from ..variable import Variable
from ...exceptions import TemplateEngineException


class FieldSelection(Expression):

    def __init__(self, line, identifier):
        super().__init__(line)
        self._target = Variable(identifier.line,
            "".join(id.image for id in identifier.identifiers[:-2]))
        self._field = identifier.identifiers[-1]

    def analyse(self, context=None):
        self.context = context
        self._target = self._target.analyse(self.context)

    def get_value(self):
        target_value = self._target.get_value()

        if isinstance(target_value, dict):
            try:
                return target_value[self._field.image]
            except KeyError:
                pass

        try:
            return getattr(target_value, self._field.image)
        except AttributeError:
            raise

    def set_value(self, value):
        target_value = self._target.get_value()
        setattr(target_value, self._field.image, value)
