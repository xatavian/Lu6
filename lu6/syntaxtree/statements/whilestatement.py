from .statement import Statement
from ..expression import BinaryExpression

class WhileStatement(Statement):
    def __init__(self, line, condition, body):
        super().__init__(line)
        self._condition = condition
        self._body = body

    def analyse(self, context=None):
        self.context = context
        self._condition.analyse(self.context)

        if self._body is not None:
            self._body.analyse(self.context)

    def codegen(self, output_stream, base_indent=0):
        while self._condition.get_value():
            if not isinstance(self._body, BinaryExpression):
                self._body.codegen(output_stream, base_indent)
            else:
                self._body.get_value()
