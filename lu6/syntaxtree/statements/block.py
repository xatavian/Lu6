from .statement import Statement
from ..expression.binaryexpression import BinaryExpression


class Block(Statement):

    def __init__(self, line, statements):
        super().__init__(line)
        self._statements = statements

    def codegen(self, output_stream, base_indent=0):
        # output_stream.print("{", "h_file", base_indent)
        for statement in self._statements:

            # In Expressions, codegen is used for printing the actual value of the expression
            # If the statement is a statement expression (therefore it is not intended to be printed), get_value()
            # is used in order to prevent the printing of the expression value
            if not isinstance(statement, BinaryExpression):
                statement.codegen(output_stream, base_indent)
            else:
                statement.get_value()

        if not output_stream.h_is_newline:
            output_stream.newline("h_file")

        # output_stream.print("}", "h_file", base_indent)

    def analyse(self, context=None):
        self.context = self.create_context(context)
        for statement in self._statements:
            statement.analyse(self.context)

    @property
    def statements(self):
        return self._statements

    def __str__(self):
        result = "BlockStatement: { "
        for statement in self._statements:
            result += str(statement)
            result += "; "
        result += "}"
        return result
