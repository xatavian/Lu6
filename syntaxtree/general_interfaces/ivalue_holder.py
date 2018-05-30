class IValueHolder(object):
    def __init__(self, value = None):
        self._value = value

    @property
    def value(self):
        return self.value

    @value.setter
    def value(self, value):
        self._value = value
