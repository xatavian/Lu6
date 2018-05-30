from ..astnode import ASTNode
from ..general_interfaces import IValueHolder


class Literal(IValueHolder, ASTNode):

    def __init__(self, line, value):
        ASTNode.__init__(self, line)
        IValueHolder.__init__(self, value)

    def __add__(self, other):
        return type(self)(self.line, self._value + other.value)

    def __iadd__(self, other):
        self._value += other.value
        return self

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return self.value

    @property
    def value(self):
        return self._value

    def codegen(self, output_stream, base_indent=0):
        output_stream.print(self.value, "h_file", base_indent)

    def analyse(self, context=None):
        pass

