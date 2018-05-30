from exceptions import TypeCheckingException


class EmptyValue(object):
    def __str__(self):
        return ""

    def __repr__(self):
        return ""


class ContextEntry(object):
    def __init__(self, line, name=None, value=None):
        if name is None:
            raise TypeCheckingException("A variable must have a name", line)
        self._name = name

        if value is not None:
            self._value = value
        else:
            self._value = EmptyValue()

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


