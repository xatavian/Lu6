from .astnode import ASTNode
from ..contexttable import Context

class FunctionDeclaration(ASTNode):
    def __init__(self, line, returnType, name, arguments, body):
        super().__init__(line)

        self._name = name
        self._returnType = returnType
        self._arguments = arguments
        self._body = body

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def returnType(self):
        return self._returnType

    @property
    def arguments(self):
        return self._arguments

    @property
    def body(self):
        return self._body

    def codegen_arguments(self, output_stream, base_indent):
        output_stream.print("(", "h_file", base_indent)

        # Print arguments
        if len(self._arguments) > 0:
            self._arguments[0].codegen(output_stream, base_indent)
        for argument in self._arguments[1:]:
            output_stream.print(", ", "h_file", base_indent)
            argument.codegen(output_stream, base_indent)

        output_stream.print(")", "h_file", base_indent)

    def codegen(self, output_stream, base_indent=0):
        if self._returnType is not None:
            self._returnType.codegen(output_stream, base_indent)
            output_stream.print(" ", "h_file", base_indent)

        self.name.codegen(output_stream, base_indent)
        self.codegen_arguments(output_stream, base_indent)

        if self._body is not None:
            output_stream.print("{", "h_file", base_indent)
            output_stream.newline("h_file")

            self._body.codegen(output_stream, base_indent + 2)

            output_stream.print("}", "h_file", base_indent)
            output_stream.newline("h_file")
        else:
            output_stream.print(";", "h_file", base_indent)

        output_stream.newline("h_file")

    def analyse(self, context=None):
        self.context = Context(context)
        for arg in self._arguments:
            arg.analyse(context)

        if self._body is not None:
            self._body.analyse(self.context)
