from .statement import Statement
from ..expression import BinaryExpression

class IfStatement(Statement):

    def __init__(self, line, condition, if_body, else_body):
        super().__init__(line)
        self._condition = condition
        self._if_body = if_body
        self._else_body = else_body
        self._toPrint = False

    def codegen(self, output_stream, base_indent=0):
        # Parsing enforces that the condition is an expression, which implements get_value
        if self._condition.get_value():
            if not isinstance(self._if_body, BinaryExpression):
                self._if_body.codegen(output_stream, base_indent)
            else:
                self._if_body.get_value()
        else:
            if not isinstance(self._else_body, BinaryExpression):
                self._else_body.codegen(output_stream, base_indent)
            else:
                self._else_body.get_value()

    def analyse(self, context=None):
        self.context = context

        self._condition.analyse(context)

        self._if_body.analyse(context)
        if self._else_body is not None:
            self._else_body.analyse(context)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        result = "IfStatement({condition}) {{ {body} }} {{ {else_body} }}".format(
            condition=self._condition,
            body=self._if_body,
            else_body=self._else_body
        )
        return result
