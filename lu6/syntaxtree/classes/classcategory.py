from ..astnode import ASTNode

class ClassCategory(ASTNode):
    def __init__(self, line, name, body):
        super().__init__(line)
        self._name = name
        self._body = body

    def analyse(self, context=None):
        print("Analysis")
        self.context = context
        self._name.analyse(self.context)

        if self._body is not None:
            self._body.analyse(self.context)

    def codegen(self, output_stream, base_indent):
        self._name.codegen(output_stream, base_indent)
        output_stream.print(":", "h_file", base_indent)
        output_stream.newline("h_file")

        if self._body is not None:
            self._body.codegen(output_stream, base_indent + 2)
